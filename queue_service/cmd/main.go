package main

import (
	"context"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"strings"

	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/s3"
	pdf "github.com/ledongthuc/pdf"
	amqp "github.com/rabbitmq/amqp091-go"
)

type Metadata struct {
	Email   string `json:"email"`
	FileURL string `json:"file_url"`
	S3Key   string `json:"s3_key"` // S3 object key to identify the file
}

const (
	rabbitMQURL   = "amqps://admin:TM61SgrKy0NexEvzg4XNW6Kmktz28vi2@s62odb.stackhero-network.com:10641"
	rabbitMQQueue = "metadata_queue"
	tempDir       = "./temp"
	s3Endpoint    = "https://3plvis.stackhero-network.com" // Custom endpoint
	s3Region      = "us-east-1"                            // Replace with the correct region
	s3BucketName  = "user-files-storage"                   // Bucket name
)

var s3Client *s3.Client

func main() {
	// Initialize S3 client with path-style addressing
	cfg, err := config.LoadDefaultConfig(context.TODO(), config.WithRegion(s3Region))
	if err != nil {
		log.Fatalf("Unable to load AWS configuration: %v", err)
	}

	s3Client = s3.NewFromConfig(cfg, func(o *s3.Options) {
		o.EndpointResolver = s3.EndpointResolverFromURL(s3Endpoint) // Use the custom endpoint
		o.UsePathStyle = true                                       // Enforce path-style addressing
	})

	log.Println("Starting RabbitMQ consumer...")
	startConsumer()
}

func startConsumer() {
	conn, err := amqp.Dial(rabbitMQURL)
	if err != nil {
		log.Fatalf("Failed to connect to RabbitMQ: %v", err)
	}
	defer conn.Close()

	ch, err := conn.Channel()
	if err != nil {
		log.Fatalf("Failed to open a channel: %v", err)
	}
	defer ch.Close()

	msgs, err := ch.Consume(
		rabbitMQQueue, // queue name
		"",            // consumer tag
		true,          // auto-ack
		false,         // exclusive
		false,         // no-local
		false,         // no-wait
		nil,           // args
	)
	if err != nil {
		log.Fatalf("Failed to register a consumer: %v", err)
	}

	log.Println("Waiting for messages...")

	forever := make(chan bool)

	go func() {
		for d := range msgs {
			log.Printf("Received a message: %s", d.Body)

			var metadata Metadata
			if err := json.Unmarshal(d.Body, &metadata); err != nil {
				log.Printf("Failed to parse metadata: %v", err)
				continue
			}

			if err := processFile(metadata); err != nil {
				log.Printf("Failed to process file: %v", err)
			} else {
				log.Printf("Successfully processed file for email: %s", metadata.Email)
			}
		}
	}()

	<-forever
}

func processFile(metadata Metadata) error {
	fileURL := metadata.FileURL
	s3Key := metadata.S3Key

	log.Printf("Downloading file from URL: %s", fileURL)
	log.Printf("Downloading file from s3key: %s", s3Key)

	resp, err := http.Get(fileURL)
	if err != nil {
		return fmt.Errorf("failed to download file: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return fmt.Errorf("unexpected HTTP status: %s", resp.Status)
	}

	// Create temp directory if not exists
	if _, err := os.Stat(tempDir); os.IsNotExist(err) {
		if err := os.Mkdir(tempDir, 0755); err != nil {
			return fmt.Errorf("failed to create temp directory: %w", err)
		}
	}

	tempFilePath := fmt.Sprintf("%s/temp_file.pdf", tempDir)
	out, err := os.Create(tempFilePath)
	if err != nil {
		return fmt.Errorf("failed to create temp file: %w", err)
	}
	defer out.Close()

	if _, err := io.Copy(out, resp.Body); err != nil {
		return fmt.Errorf("failed to save file: %w", err)
	}

	log.Printf("File downloaded to: %s", tempFilePath)

	processingResult := processDownloadedFile(tempFilePath)
	log.Printf("Processing result: %s", processingResult)

	// Delete temp file
	if err := os.Remove(tempFilePath); err != nil {
		log.Printf("Warning: failed to delete temp file: %v", err)
	}

	return nil
}

func processDownloadedFile(filePath string) []string {
	file, err := os.Open(filePath)
	if err != nil {
		log.Printf("Failed to open file: %v", err)
		return nil
	}
	defer file.Close()

	// Get file information (size, etc.)
	fileInfo, err := file.Stat()
	if err != nil {
		log.Printf("Failed to get file info: %v", err)
		return nil
	}

	// Use the pdf library to extract text
	reader, err := pdf.NewReader(file, fileInfo.Size())
	if err != nil {
		log.Printf("Failed to create PDF reader: %v", err)
		return nil
	}

	var text string
	for pageIndex := 1; pageIndex <= reader.NumPage(); pageIndex++ {
		page := reader.Page(pageIndex)
		if page.V.IsNull() {
			continue
		}

		pageText, err := page.GetPlainText(nil)
		if err != nil {
			log.Printf("Failed to extract text from page %d: %v", pageIndex, err)
			continue
		}

		text += pageText
	}

	if text == "" {
		log.Println("No text found in the file.")
		return nil
	}

	chunks := splitTextIntoChunks(text, 200)

	return chunks
}

func splitTextIntoChunks(text string, chunkSize int) []string {
	words := strings.Fields(text) // Split text into words
	var chunks []string

	for i := 0; i < len(words); i += chunkSize {
		end := i + chunkSize
		if end > len(words) {
			end = len(words)
		}
		chunks = append(chunks, strings.Join(words[i:end], " "))
	}

	return chunks
}

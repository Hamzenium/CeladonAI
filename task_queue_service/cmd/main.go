package main

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"strings"

	"cloud.google.com/go/firestore"
	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/s3"
	pdf "github.com/ledongthuc/pdf"
	amqp "github.com/rabbitmq/amqp091-go"
	"google.golang.org/api/option"
)

type Metadata struct {
	Email      string `json:"email"`
	FileURL    string `json:"file_url"`
	S3Key      string `json:"s3_key"`
	DocumentID string `json:"document_id"` // Capitalized for export
}

const (
	rabbitMQURL   = "amqps://admin:TM61SgrKy0NexEvzg4XNW6Kmktz28vi2@s62odb.stackhero-network.com:10641"
	rabbitMQQueue = "metadata_queue"
	tempDir       = "./temp"
	s3Endpoint    = "https://3plvis.stackhero-network.com"
	s3Region      = "us-east-1"
	s3BucketName  = "user-files-storage"
)

var (
	s3Client        *s3.Client
	firestoreClient *firestore.Client
)

func main() {
	ctx := context.Background()

	// Initialize Firestore client using service account JSON
	serviceAccountConfig := `{
		"type": "service_account",
		"project_id": "celadonai-69915",
		"private_key_id": "8f804db31dc592456d7069d88cb202409cb35dfb",
		"private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDADFrzn3Miez/C\nRKOPWX6HGiMRvFgz01mdYa8eX9jSBgUH9XhrS36UjhfapYvzjClclAZPDRYrIXjp\nOHiEnHrfrxT2+6LQCSoBOJnxQSfUiGQc2ch77KNkzs20z7h2LipvZeBK7Y+5SAD9\n7rQh8OMiQlN+HkRN6eL9QtR4J8Yt5cHncvH+mpFgBC1OeGwCPW8+K2WRG4UwYIdL\nQiIhzHanoJgkK0NznYjOyLyRZiLsnCv2RTfuFsaJvjB8AKTVuckOJTk4YI4LDpyt\nkc7FQGTCvvYJBLIi3QjEvc+IbOOdoAGMeU43N/wD67b+9w+UsBkuoILMLDP9+agf\nInH6LVndAgMBAAECggEAEaQw6KcxgtiH2KxzH98XMzQ7RiJN3I43cbBq+eMmaNM6\nZsBC9ww2IlGpLvcSaOVrrpWUZ3JAIpHOaGdnvrrHGMFzBLsZz3rABouwrHY76+yO\n0bhPD9SC2pGarizUo4Uwdbo0hSgsZyyOQW/00RdZLf5MwCLp9a7x9dTL7Vut+0Iy\niZnCWjCkuLuB4R1da27LGMSK/bB5uxA8I3495FGLGnI1OUONGQaqUN25TXQBekZ3\nsUl7u3Pn78LCYsl3M1Yr0RMGj4yf7ZymohYQCIKYkKBnD6GvgR9ePSVe8wTYLHYU\nWc/KUYPbo+ekcow+n2sOUukrJSLDOBc4GsrZSuw2qwKBgQDhzR9dCkUwHIYHtjyS\nIBDIB2VSxjdj9idWKzYMsmofbmbVfk9PklbO/tRFOpGlIUffsWUFt5iSNEgQSjDQ\n0jJUnkAWTeRxVVFw+CKPrHcuVGZvrux+ja03tGSMA5P8Q8yvTFXj2QzdCNInej4Q\nD6SmbNK/DrGj6v+EUiQWQgH52wKBgQDZu50Oy0/9ghs3u6GqaEHD1HBQM3ydwa1Z\n396qisINAYGcdKeVXiEDlSSWunUHTdgUksk0Q4jpM5NrGvKMocXCgA+P78HH+nfW\n66TdI+ok4WqahVoZtUiQdJ1wfhLR5+o1AYQhVaKK1paZ0oadSj+ATzIN8f/fsSAi\nMtNkOg7UpwKBgBzdlhbUy0d9Pf0aZN/hTYPkviU4xbf3rcusNnqlDD/8YxUD0qu/\nb22C0iwPcrMDcCa+jMWQVObL3DKI6Xiohlqe6F5xkrSSTZj9f52SVKINlBLO79i1\nz+EBJKFpi6+CE1aNkaVRB/3xtLvrOqfe+BN2cfKOtFLaJdQKlCZsRchlAoGAIfXf\nY2VWzqWydRjw+FFWoKLL+dZuA3UoArKmWldWOQ0ZGDwhv2x1HcfvcwsWIdOEdoEG\nnP5DpowC3FvRpRm+bL3or3yn7vckJgOPLWbiqGn4ZK2UBhp+fPmTbO5dJRxVLXtV\nDpX6ykj6KHfrwzDHgs3XctFiJZPM/UiMLD/Z/FUCgYANnxxRddHriNXSSZ1xNiaa\nLj1Wmk02RIZeMBy4mYEAoLkv5pjOct+cqCX5DAuNeYCf+Z7J4FnJEcp4mzAqczCr\nsjGGnbvBIta15o7xUktSrurQ5k9wW40i+V3yR/EoGOrl3CSMaIb5YPDFx4dV5yH5\nSKHQkyyLHR/TagMyFma5xA==\n-----END PRIVATE KEY-----\n",
		"client_email": "firebase-adminsdk-b5q1e@celadonai-69915.iam.gserviceaccount.com",
		"client_id": "105666354436499285256",
		"auth_uri": "https://accounts.google.com/o/oauth2/auth",
		"token_uri": "https://oauth2.googleapis.com/token",
		"auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
		"client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-b5q1e@celadonai-69915.iam.gserviceaccount.com"
	}`

	var err error
	firestoreClient, err = firestore.NewClient(ctx, "celadonai-69915", option.WithCredentialsJSON([]byte(serviceAccountConfig)))
	if err != nil {
		log.Fatalf("Failed to initialize Firestore client: %v", err)
	}
	defer firestoreClient.Close()

	// Initialize S3 client
	cfg, err := config.LoadDefaultConfig(ctx, config.WithRegion(s3Region))
	if err != nil {
		log.Fatalf("Unable to load AWS configuration: %v", err)
	}

	s3Client = s3.NewFromConfig(cfg, func(o *s3.Options) {
		o.EndpointResolver = s3.EndpointResolverFromURL(s3Endpoint)
		o.UsePathStyle = true
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
		rabbitMQQueue,
		"",
		true,
		false,
		false,
		false,
		nil,
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
	log.Printf("Downloading file from URL: %s", fileURL)

	// Download the file
	resp, err := http.Get(fileURL)
	if err != nil {
		return fmt.Errorf("failed to download file: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return fmt.Errorf("unexpected HTTP status: %s", resp.Status)
	}

	// Save the file temporarily
	tempFilePath := "./temp_file.pdf"
	out, err := os.Create(tempFilePath)
	if err != nil {
		return fmt.Errorf("failed to create temp file: %w", err)
	}
	defer out.Close()

	if _, err := io.Copy(out, resp.Body); err != nil {
		return fmt.Errorf("failed to save file: %w", err)
	}

	log.Printf("File downloaded to: %s", tempFilePath)

	// Process the downloaded PDF file to extract paragraphs and embeddings
	paragraphs, embeddings := processDownloadedFile(tempFilePath)
	if paragraphs == nil || embeddings == nil {
		return fmt.Errorf("file processing failed")
	}

	// Convert embeddings ([][]float32) to JSON string
	embeddingsJSON, err := json.Marshal(embeddings)
	if err != nil {
		return fmt.Errorf("failed to convert embeddings to JSON: %w", err)
	}

	doc_id := metadata.DocumentID
	documentName := metadata.S3Key
	data := map[string]interface{}{
		"embeddings":  string(embeddingsJSON), // Store embeddings as JSON string
		"paragraphs":  paragraphs,
		"name":        documentName,
		"document_id": doc_id,
		"file_url":    fileURL,
	}

	// Save the data to Firestore
	if err := saveToFirebase(metadata.Email, data, doc_id); err != nil {
		return fmt.Errorf("failed to save data to Firebase: %w", err)
	}

	log.Printf("File processed and saved to Firebase for email: %s", metadata.Email)
	return nil
}

func processDownloadedFile(filePath string) ([]string, [][]float64) {
	file, err := os.Open(filePath)
	if err != nil {
		log.Printf("Failed to open file: %v", err)
		return nil, nil
	}
	defer file.Close()

	// Get file information (size, etc.)
	fileInfo, err := file.Stat()
	if err != nil {
		log.Printf("Failed to get file info: %v", err)
		return nil, nil
	}

	// Use the pdf library to extract text
	reader, err := pdf.NewReader(file, fileInfo.Size())
	if err != nil {
		log.Printf("Failed to create PDF reader: %v", err)
		return nil, nil
	}

	var text string
	// Loop through each page to extract text
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
		return nil, nil
	}

	// Split the extracted text into chunks
	chunks := splitTextIntoChunks(text, 200)

	// Get embeddings for the chunks
	embeddings := getEmbeddings(chunks)
	fmt.Print(chunks, embeddings)
	// Return both chunks and embeddings
	return chunks, embeddings
}

func getEmbeddings(textChunks []string) [][]float64 {
	url := "https://api.openai.com/v1/embeddings"
	embeddings := [][]float64{}
	for _, chunk := range textChunks {
		payload := fmt.Sprintf(`{"input": "%s", "model": "text-embedding-ada-002"}`, chunk)
		apiKey := "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"
		req, _ := http.NewRequest("POST", url, bytes.NewBuffer([]byte(payload)))
		req.Header.Set("Authorization", "Bearer "+apiKey)
		req.Header.Set("Content-Type", "application/json")

		resp, _ := http.DefaultClient.Do(req)
		if resp.StatusCode != http.StatusOK {
			continue
		}
		defer resp.Body.Close()

		body, _ := io.ReadAll(resp.Body)

		var result map[string]interface{}
		json.Unmarshal(body, &result)

		for _, item := range result["data"].([]interface{}) {
			embedding := item.(map[string]interface{})["embedding"].([]interface{})
			emb := make([]float64, len(embedding))
			for i, val := range embedding {
				emb[i] = float64(val.(float64))
			}
			embeddings = append(embeddings, emb)
		}
	}

	return embeddings
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

func saveToFirebase(email string, data map[string]interface{}, doc_id string) error {
	ctx := context.Background()
	// Save data to Firestore under "users" collection with documentID
	_, err := firestoreClient.Collection("users").Doc(doc_id).Set(ctx, data)
	if err != nil {
		return fmt.Errorf("failed to save document: %w", err)
	}

	return nil
}

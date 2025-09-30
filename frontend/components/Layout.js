import { AuthContextProvider } from '/utils/AuthContext'

export default function Layout({ children }) {
    return (
        <AuthContextProvider>
            <main>{children}</main>
        </AuthContextProvider>
    )
}
import Link from 'next/link';
import styles from '../styles/Navbar.module.css';
import { useAuthContext } from "/utils/AuthContext";
import firebase_app from "/utils/firebaseconfig.js";
import { signOut, getAuth } from "firebase/auth";

const auth = getAuth(firebase_app);

const Navbar = () => {
    const { user } = useAuthContext()

    const handleSignOut = async () => {
        let result = null,
            error = null;
        try {
            result = await signOut(auth);
        } catch (e) {
            error = e;
        }

        console.log({ result, error });
    }

    return (
        <>
            <nav className={styles.navbar}>
                <div className={styles.navBrand}>
                    <a href='/'><img src="/celai.png" alt="Logo" className={styles.brandLogo} /></a>
                </div>
                <ul className={styles.navList}>
                    <li className={styles.navItem}>
                        <Link href="/" className={styles.navLink}>
                            Home
                        </Link>
                    </li>
                    <li className={styles.navItem}>
                        <Link href="/chatbots" className={styles.navLink}>
                            Chatbots
                        </Link>
                    </li>
                    <li className={styles.navItem}>
                        <Link href="/guide" className={styles.navLink}>
                            Guide
                        </Link>
                    </li>
                </ul>

                <div className={styles.authButtons}>
                    {user ?
                        <button className={styles.logout} onClick={handleSignOut}>Logout</button>
                        :
                        <>
                            <Link href="/auth/login"><button className={styles.authButton}>Login</button></Link>
                            <Link href="/auth/signup"><button className={styles.authButton}>Sign Up</button></Link>
                        </>
                    }
                </div>
            </nav>
            <ul className={styles.navListMobile}>
                <li className={styles.navItem}>
                    <Link href="/" className={styles.navLink}>
                        Home
                    </Link>
                </li>
                <li className={styles.navItem}>
                    <Link href="/chatbots" className={styles.navLink}>
                        Chatbots
                    </Link>
                </li>
                <li className={styles.navItem}>
                    <Link href="/guide" className={styles.navLink}>
                        Guide
                    </Link>
                </li>
            </ul>
        </>
    );
};

export default Navbar;

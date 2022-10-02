import Head from "next/head";
import styles from "../styles/Home.module.css";
import Navbar from "../components/Navbar";
import Articles from "../components/Article";

export default function Home() {
  return (
    <div className={styles.container}>
      <Head>
        <title>NASA Challenge</title>
        <meta name="description" content="Generated by create next app" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <Navbar />
      <Articles />
    </div>
  );
}

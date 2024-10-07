import Head from 'next/head';
import VideoDownloader from '../components/VideoDownloader';

export default function Home() {
    return (
        <div>
            <Head>
                <title>YouTube Video Downloader</title>
                <meta name="description" content="Download YouTube videos in various qualities." />
                <link rel="icon" href="/favicon.ico" />
            </Head>

            <main>
                <VideoDownloader />
            </main>
        </div>
    );
}

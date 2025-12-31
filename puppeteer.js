import puppeteer from "puppeteer";
import { spawn } from "child_process";

async function recordWebpage(url, output = "output.mp4", duration = 10, fps = 30) {
  const width = 1280;
  const height = 720;

  // Launch headless Chromium
  const browser = await puppeteer.launch({
    headless: true,
    defaultViewport: { width, height },
    args: [`--window-size=${width},${height}`],
  });
  const page = await browser.newPage();
  await page.goto(url, { waitUntil: "networkidle0" });

  const iframe = await page.waitForSelector("iframe");
  const frame = await iframe.contentFrame();

  await frame.waitForNavigation({ waitUntil: "networkidle0" });
  await frame.click("button[title='play']");

  // FFmpeg setup — receives PNG frames via stdin
  const ffmpeg = spawn("ffmpeg", [
    "-y", // overwrite output
    "-f", "image2pipe",
    "-vcodec", "png",
    "-r", String(fps),
    "-i", "-",
    "-pix_fmt", "yuv420p",
    "-vcodec", "libx264",
    output,
  ]);

  ffmpeg.stderr.on("data", (data) => {
    console.error("FFmpeg error:", data);
  });

  console.log(`🎥 Recording ${duration}s of ${url} ...`);

  const frameInterval = 1000 / fps;
  const start = Date.now();

  const captureFrame = async () => {
    const buffer = await page.screenshot({ type: "png" });
    ffmpeg.stdin.write(buffer);
  };

  while (Date.now() - start < duration * 1000) {
    await captureFrame();
    await new Promise((r) => setTimeout(r, frameInterval));
  }

  ffmpeg.stdin.end();
  await browser.close();

  // Wait for ffmpeg to finish writing file
  await new Promise((resolve) => ffmpeg.on("close", resolve));

  console.log(`✅ Saved video: ${output}`);
}

// Example usage
recordWebpage(
  "file:///Users/geronimodiaz/projects/m2d2/output.html",
  "output.mp4",
  10
).catch(console.error);

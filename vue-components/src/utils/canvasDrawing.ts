import { HistogramData } from './types';
import clamp from './clamp';

const BAR_GAP = 2;

export function drawHistogram(
  histogramData: HistogramData,
  canvas: HTMLCanvasElement,
  dark = false
) {
  const context = canvas.getContext('2d');
  if (!context) return;
  if (dark) context.fillStyle = 'white';
  const { width, height } = canvas;

  const numBuckets = histogramData.counts.length;
  const barWidth = width / numBuckets;
  const maxBucketCount = Math.max(...histogramData.counts);

  histogramData.counts.forEach((count, index) => {
    const barHeight = height * (count / maxBucketCount);
    const startX = index * barWidth;
    const startY = height - barHeight;

    context.beginPath();
    context.rect(startX + BAR_GAP, startY, barWidth - BAR_GAP, barHeight);
    context.fill();
  });
}

export function drawLabels(histogramData: HistogramData, labelsDiv: Element) {
  labelsDiv.innerHTML = '';

  const labels = histogramData.range;
  labels.forEach((barLabel) => {
    const label = document.createElement('p');
    label.innerHTML = `${barLabel}`;
    label.style.textAlign = 'center';
    labelsDiv.appendChild(label);
  });
}

export function drawGradient(
  colorNodes: Array<Array<number>>,
  canvas: HTMLCanvasElement,
  fullRange: Array<number>,
  crop: number
) {
  if (!canvas) return;
  const context = canvas.getContext('2d');
  if (!context) return;
  const { width, height } = canvas;

  const gradient = context.createLinearGradient(0, 0, width, 0);
  colorNodes.forEach((node) => {
    const scalarValue = Math.floor(node[0]);
    const proportion = clamp(
      (scalarValue - fullRange[0]) / (fullRange[1] - fullRange[0]),
      0,
      1
    );
    const rgb = node.slice(1).map((value) => value * 255);
    gradient.addColorStop(proportion, `rgb(${rgb[0]}, ${rgb[1]}, ${rgb[2]})`);
  });

  context.fillStyle = gradient;
  context.fillRect(0, 0, width, height);

  // crop to indentation of histogram
  const cropProportion = (crop - fullRange[0]) / (fullRange[1] - fullRange[0]);
  crop = cropProportion * width;
  context.clearRect(0, 0, crop, height);
  context.clearRect(width - crop, 0, crop, height);
}

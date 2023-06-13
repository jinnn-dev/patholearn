interface Point {
  x: number;
  y: number;
}
function lerp(start: number, end: number, t: number): number {
  return start * (1 - t) + end * t;
}

function easeInOut(t: number): number {
  return t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
}

export function animateBetweenTwoPoints(
  start: Point,
  end: Point,
  duration: number,
  callback: (x: number, y: number) => Promise<void>
): Promise<void> {
  const frames = 30;
  const steps = duration * frames; // Assuming 60 frames per second.

  return new Promise((resolve) => {
    let t = 0;
    const intervalId = setInterval(async () => {
      if (t > 1) {
        clearInterval(intervalId);
        resolve();
      } else {
        const easedT = t;
        const x = lerp(start.x, end.x, easedT);
        const y = lerp(start.y, end.y, easedT);

        await callback(x, y);
        t += 1 / steps;
      }
    }, 1000 / frames); // Running this each frame (1/60th of a second)
  });
}

export function calculatePointsBetween(start: Point, end: Point, steps: number): Point[] {
  const points: Point[] = [];

  for (let i = 0; i <= steps; i++) {
    const t = i / steps;
    const x = lerp(start.x, end.x, t);
    const y = lerp(start.y, end.y, t);
    points.push({ x, y });
  }

  return points;
}

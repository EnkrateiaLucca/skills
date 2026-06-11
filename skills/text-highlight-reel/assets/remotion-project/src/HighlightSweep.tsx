import {
  AbsoluteFill,
  Easing,
  Img,
  interpolate,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { z } from "zod";

export const lineSchema = z.object({
  x: z.number(),
  y: z.number(),
  w: z.number(),
  h: z.number(),
});

export const highlightSchema = z.object({
  imageSrc: z.string(),
  imageWidth: z.number(),
  imageHeight: z.number(),
  lines: z.array(lineSchema),
  // Optional padded "stay sharp" rectangles. If omitted, computed from lines.
  sharpRects: z
    .array(z.object({ x: z.number(), y: z.number(), w: z.number(), h: z.number(), r: z.number() }))
    .optional(),
  durationSeconds: z.number().default(6),
  // Animation phase timings (seconds)
  blurStart: z.number().default(0.5),
  blurEnd: z.number().default(1.5),
  sweepStart: z.number().default(1.6),
  sweepEnd: z.number().default(4.6),
  // Visuals
  blurRadius: z.number().default(10),
  dim: z.number().default(0.45),
  highlightColorA: z.string().default("rgba(255,225,80,0.85)"),
  highlightColorB: z.string().default("rgba(255,235,120,0.92)"),
});

export type HighlightProps = z.infer<typeof highlightSchema>;

export const defaultProps: HighlightProps = {
  imageSrc: "source.png",
  imageWidth: 1920,
  imageHeight: 1080,
  lines: [{ x: 100, y: 100, w: 800, h: 60 }],
  durationSeconds: 6,
  blurStart: 0.5,
  blurEnd: 1.5,
  sweepStart: 1.6,
  sweepEnd: 4.6,
  blurRadius: 10,
  dim: 0.45,
  highlightColorA: "rgba(255,225,80,0.85)",
  highlightColorB: "rgba(255,235,120,0.92)",
};

const padRect = (l: { x: number; y: number; w: number; h: number }) => ({
  x: l.x - 25,
  y: l.y - 17,
  w: l.w + 50,
  h: l.h + 30,
  r: 14,
});

export const HighlightSweep: React.FC<HighlightProps> = (props) => {
  const frame = useCurrentFrame();
  const { fps, width: W, height: H } = useVideoConfig();
  const src = staticFile(props.imageSrc);
  const t = frame / fps;

  const sharpRects = props.sharpRects ?? props.lines.map(padRect);
  const totalW = props.lines.reduce((s, l) => s + l.w, 0);

  const blurAmount = interpolate(
    t,
    [props.blurStart, props.blurEnd],
    [0, props.blurRadius],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.inOut(Easing.quad) },
  );
  const dimAmount = interpolate(t, [props.blurStart, props.blurEnd], [0, props.dim], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.inOut(Easing.quad),
  });
  const sweep = interpolate(t, [props.sweepStart, props.sweepEnd], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.inOut(Easing.cubic),
  });
  const sharpReveal = interpolate(t, [props.blurStart, props.blurEnd - 0.2], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  let consumed = 0;
  const lineFills = props.lines.map((l) => {
    const remaining = Math.max(0, sweep * totalW - consumed);
    const fill = Math.min(remaining, l.w);
    consumed += l.w;
    return fill;
  });

  return (
    <AbsoluteFill style={{ backgroundColor: "white" }}>
      <Img
        src={src}
        style={{
          width: W,
          height: H,
          filter: `blur(${blurAmount}px) brightness(${1 - dimAmount * 0.35})`,
        }}
      />

      {sharpRects.map((r, i) => (
        <div
          key={i}
          style={{
            position: "absolute",
            left: r.x,
            top: r.y,
            width: r.w,
            height: r.h,
            overflow: "hidden",
            borderRadius: r.r,
            WebkitMaskImage:
              "radial-gradient(ellipse at center, black 70%, transparent 100%)",
            maskImage:
              "radial-gradient(ellipse at center, black 70%, transparent 100%)",
            opacity: sharpReveal,
          }}
        >
          <Img
            src={src}
            style={{
              width: W,
              height: H,
              position: "absolute",
              left: -r.x,
              top: -r.y,
            }}
          />
        </div>
      ))}

      {props.lines.map((l, i) => (
        <div
          key={i}
          style={{
            position: "absolute",
            left: l.x,
            top: l.y,
            width: lineFills[i],
            height: l.h,
            background: `linear-gradient(90deg, ${props.highlightColorA}, ${props.highlightColorB})`,
            mixBlendMode: "multiply",
            borderRadius: 4,
            boxShadow: "inset 0 -3px 0 rgba(230,180,0,0.25)",
          }}
        />
      ))}

      {props.lines.map((l, i) => {
        const fill = lineFills[i];
        if (fill <= 0 || fill >= l.w) return null;
        return (
          <div
            key={`caret-${i}`}
            style={{
              position: "absolute",
              left: l.x + fill - 30,
              top: l.y - 4,
              width: 60,
              height: l.h + 8,
              background:
                "linear-gradient(90deg, rgba(255,200,0,0) 0%, rgba(255,200,0,0.5) 70%, rgba(255,200,0,0) 100%)",
              mixBlendMode: "multiply",
              filter: "blur(6px)",
            }}
          />
        );
      })}
    </AbsoluteFill>
  );
};

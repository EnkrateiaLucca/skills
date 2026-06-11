import { Composition } from "remotion";
import {
  HighlightSweep,
  highlightSchema,
  defaultProps,
} from "./HighlightSweep";

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="Highlight"
      component={HighlightSweep}
      schema={highlightSchema}
      defaultProps={defaultProps}
      fps={30}
      width={1920}
      height={1080}
      durationInFrames={180}
      calculateMetadata={({ props }) => {
        const fps = 30;
        const even = (n: number) => (n % 2 ? n - 1 : n);
        return {
          width: even(props.imageWidth),
          height: even(props.imageHeight),
          durationInFrames: Math.round((props.durationSeconds ?? 6) * fps),
          fps,
        };
      }}
    />
  );
};

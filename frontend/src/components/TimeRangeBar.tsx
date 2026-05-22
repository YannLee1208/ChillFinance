import type { TimeRangeKey } from "./timeRange";
import { TIME_RANGE_OPTIONS } from "./timeRange";

type TimeRangeBarProps = {
  value: TimeRangeKey;
  onChange: (value: TimeRangeKey) => void;
};

export function TimeRangeBar({ value, onChange }: TimeRangeBarProps) {
  return (
    <section className="time-range-bar" aria-label="时间范围">
      <div>
        <span>时间窗口</span>
        <strong>默认只展示近3年，避免长序列压缩图形</strong>
      </div>
      <div className="range-tabs">
        {TIME_RANGE_OPTIONS.map((option) => (
          <button
            className={option.key === value ? "active" : ""}
            key={option.key}
            onClick={() => onChange(option.key)}
            type="button"
          >
            {option.label}
          </button>
        ))}
      </div>
    </section>
  );
}

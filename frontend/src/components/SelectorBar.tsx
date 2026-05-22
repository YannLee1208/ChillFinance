import type { IndicatorDefinition } from "../types";
import { localizeSelectorValue } from "./localization";

const SELECTOR_LABELS: Record<string, string> = {
  category: "专题",
  commodity: "品种",
  country: "国家/地区",
  metric: "指标",
  tenor: "期限",
};

type SelectorBarProps = {
  indicators: IndicatorDefinition[];
  selected: Record<string, string>;
  onChange: (nextSelected: Record<string, string>) => void;
};

function buildOptions(indicators: IndicatorDefinition[]): Record<string, string[]> {
  const values: Record<string, Set<string>> = {};
  for (const indicator of indicators) {
    for (const [key, value] of Object.entries(indicator.selectors)) {
      values[key] = values[key] ?? new Set<string>();
      values[key].add(value);
    }
  }

  return Object.fromEntries(
    Object.entries(values)
      .map(([key, set]) => [key, Array.from(set).sort()])
      .filter(([, options]) => options.length > 1),
  );
}

export function SelectorBar({ indicators, selected, onChange }: SelectorBarProps) {
  const optionsByKey = buildOptions(indicators);
  const selectorKeys = Object.keys(optionsByKey).sort((left, right) => {
    const order = ["country", "category", "commodity", "metric", "tenor"];
    return order.indexOf(left) - order.indexOf(right);
  });

  if (selectorKeys.length === 0) {
    return null;
  }

  const setSelector = (key: string, value: string) => {
    const nextSelected = { ...selected };
    if (value === "") {
      delete nextSelected[key];
    } else {
      nextSelected[key] = value;
    }
    onChange(nextSelected);
  };

  const clearAll = () => onChange({});
  const hasActiveSelector = Object.keys(selected).length > 0;

  return (
    <section className="selector-bar" aria-label="板块筛选">
      <div className="selector-groups">
        {selectorKeys.map((key) => (
          <label className="selector-control" key={key}>
            <span>{SELECTOR_LABELS[key] ?? key}</span>
            <select
              onChange={(event) => setSelector(key, event.target.value)}
              value={selected[key] ?? ""}
            >
              <option value="">全部</option>
              {optionsByKey[key].map((value) => (
                <option key={value} value={value}>
                  {localizeSelectorValue(value)}
                </option>
              ))}
            </select>
          </label>
        ))}
      </div>
      <button
        className="clear-filter-button"
        disabled={!hasActiveSelector}
        onClick={clearAll}
        type="button"
      >
        清空
      </button>
    </section>
  );
}

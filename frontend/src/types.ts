export type Frequency = "daily" | "weekly" | "monthly" | "quarterly" | "annual";

export type IndicatorDefinition = {
  code: string;
  name: string;
  domain: string;
  region: string;
  unit: string;
  frequency: Frequency;
  provider: string;
  source: string;
  description: string;
  display_order: number;
};

export type Observation = {
  indicator_code: string;
  period: string;
  value: string;
  provider: string;
  source: string;
  ingested_at: string;
};

export type IndicatorSnapshot = {
  definition: IndicatorDefinition;
  latest: Observation | null;
  previous: Observation | null;
  points: Observation[];
};

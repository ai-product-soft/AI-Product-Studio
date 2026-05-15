import { MarketResearchPanel } from '@/components/analysis/MarketResearchPanel';
import { CompetitorMatrix } from '@/components/analysis/CompetitorMatrix';

export default function AnalysisPage() {
  return (
    <div className="space-y-6 p-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Market Analysis</h1>
        <p className="text-sm text-gray-500">AI-powered research & competitor intelligence</p>
      </div>
      <MarketResearchPanel />
      <CompetitorMatrix />
    </div>
  );
}

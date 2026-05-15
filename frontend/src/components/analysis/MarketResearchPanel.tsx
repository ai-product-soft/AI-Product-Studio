import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Search, BarChart3, Globe, Target, TrendingUp, Download } from 'lucide-react';

interface ResearchResult { section: string; content: string; icon: React.ReactNode; }

export function MarketResearchPanel() {
  const [query, setQuery] = useState('');
  const [isResearching, setIsResearching] = useState(false);
  const [results, setResults] = useState<ResearchResult[] | null>(null);

  const handleResearch = () => {
    if (!query.trim()) return;
    setIsResearching(true);
    setTimeout(() => {
      setResults([
        { section: 'Market Overview', content: `The ${query} market is valued at $12.4B globally with 18% YoY growth. Key drivers include AI integration and mobile-first adoption.`, icon: <Globe className="w-5 h-5" /> },
        { section: 'Competitor Analysis', content: 'Top 3 competitors: Company A (32% share), Company B (24% share), Company C (18% share). Differentiation opportunities in UX and pricing.', icon: <Target className="w-5 h-5" /> },
        { section: 'Target Audience', content: 'Primary: SMEs (40%), Enterprise (35%), Startups (25%). Pain points: cost, complexity, integration. Budget range: $500-$5,000/month.', icon: <BarChart3 className="w-5 h-5" /> },
        { section: 'Trends & Opportunities', content: 'Emerging: AI automation, no-code platforms, API-first architecture. Risk: market saturation in 2-3 years. Opportunity: vertical-specific solutions.', icon: <TrendingUp className="w-5 h-5" /> },
      ]);
      setIsResearching(false);
    }, 3000);
  };

  return (
    <div className="space-y-4">
      <Card>
        <CardHeader><CardTitle className="flex items-center gap-2"><Search className="w-5 h-5" />Market Research Engine</CardTitle></CardHeader>
        <CardContent className="space-y-4">
          <div className="flex gap-2">
            <Input placeholder="Enter product idea, industry, or competitor..." value={query} onChange={(e) => setQuery(e.target.value)} className="flex-1" />
            <Button onClick={handleResearch} disabled={isResearching}>{isResearching ? 'Researching...' : 'Research'}</Button>
          </div>
          <Textarea placeholder="Additional context (target market, budget, timeline...)" className="h-24" />
        </CardContent>
      </Card>

      {results && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {results.map((result, idx) => (
            <Card key={idx} className="hover:shadow-md transition-shadow">
              <CardHeader className="pb-2"><CardTitle className="text-base flex items-center gap-2">{result.icon}{result.section}</CardTitle></CardHeader>
              <CardContent><p className="text-sm text-gray-600 leading-relaxed">{result.content}</p></CardContent>
            </Card>
          ))}
          <div className="md:col-span-2 flex justify-end">
            <Button variant="outline" className="gap-2"><Download className="w-4 h-4" />Export Report</Button>
          </div>
        </div>
      )}
    </div>
  );
}

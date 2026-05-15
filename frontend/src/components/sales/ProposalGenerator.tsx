import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { FileText, Download, Sparkles, Loader2 } from 'lucide-react';

interface ProposalSection { title: string; content: string; }

export function ProposalGenerator() {
  const [clientName, setClientName] = useState('');
  const [projectType, setProjectType] = useState('');
  const [scope, setScope] = useState('');
  const [budget, setBudget] = useState('');
  const [timeline, setTimeline] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [proposal, setProposal] = useState<ProposalSection[] | null>(null);

  const projectTypes = ['Web Application', 'Mobile App', 'E-commerce Platform', 'SaaS Dashboard', 'AI Integration', 'Custom Software'];

  const handleGenerate = () => {
    if (!clientName || !projectType) return;
    setIsGenerating(true);
    setTimeout(() => {
      setProposal([
        { title: 'Executive Summary', content: `We propose to develop a ${projectType} for ${clientName} that addresses their specific business needs.` },
        { title: 'Scope of Work', content: scope || '• Discovery & Planning\n• UI/UX Design\n• Development\n• Testing\n• Deployment' },
        { title: 'Timeline', content: timeline || '6-8 weeks' },
        { title: 'Investment', content: budget || '$8,500' },
        { title: 'Why Choose Us', content: '• AI-Powered Development\n• Proven Track Record\n• Dedicated Support' },
        { title: 'Next Steps', content: '1. Review proposal\n2. Sign agreement\n3. Start project' },
      ]);
      setIsGenerating(false);
    }, 2000);
  };

  return (
    <div className="space-y-4">
      <Card>
        <CardHeader><CardTitle className="flex items-center gap-2"><Sparkles className="w-5 h-5 text-purple-500" />AI Proposal Generator</CardTitle></CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2"><Label>Client Name</Label><Input value={clientName} onChange={(e) => setClientName(e.target.value)} placeholder="Acme Corp" /></div>
            <div className="space-y-2">
              <Label>Project Type</Label>
              <select value={projectType} onChange={(e) => setProjectType(e.target.value)} className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm">
                <option value="">Select type...</option>
                {projectTypes.map((type) => <option key={type} value={type}>{type}</option>)}
              </select>
            </div>
          </div>
          <div className="space-y-2"><Label>Custom Scope</Label><Textarea value={scope} onChange={(e) => setScope(e.target.value)} placeholder="Enter scope..." className="h-24" /></div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2"><Label>Budget</Label><Input value={budget} onChange={(e) => setBudget(e.target.value)} placeholder="$5,000" /></div>
            <div className="space-y-2"><Label>Timeline</Label><Input value={timeline} onChange={(e) => setTimeline(e.target.value)} placeholder="6 weeks" /></div>
          </div>
          <Button onClick={handleGenerate} disabled={isGenerating || !clientName || !projectType} className="w-full gap-2">
            {isGenerating ? <><Loader2 className="w-4 h-4 animate-spin" />Generating...</> : <><Sparkles className="w-4 h-4" />Generate Proposal</>}
          </Button>
        </CardContent>
      </Card>
      {proposal && (
        <Card className="border-2 border-blue-200">
          <CardHeader className="border-b bg-blue-50 flex flex-row items-center justify-between">
            <CardTitle className="flex items-center gap-2"><FileText className="w-5 h-5" />Proposal</CardTitle>
            <Button variant="outline" size="sm" className="gap-2"><Download className="w-4 h-4" />Export PDF</Button>
          </CardHeader>
          <CardContent className="p-6 space-y-6">
            {proposal.map((section, idx) => (
              <div key={idx} className="space-y-2">
                <h3 className="text-lg font-bold text-blue-900 border-b pb-1">{section.title}</h3>
                <p className="text-sm text-gray-700 whitespace-pre-wrap">{section.content}</p>
              </div>
            ))}
            <div className="pt-4 border-t flex justify-end">
              <Button>Send to Client</Button>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}

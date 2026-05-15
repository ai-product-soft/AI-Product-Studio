import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
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
  const [proposal, setProposal] = useState<<ProposalSection[] | null>(null);

  const handleGenerate = () => {
    if (!clientName || !projectType) return;
    setIsGenerating(true);
    setTimeout(() => {
      setProposal([
        { title: 'Executive Summary', content: `We propose to develop a ${projectType} for ${clientName} that addresses their specific business needs. This solution will deliver measurable ROI within the first quarter of deployment.` },
        { title: 'Scope of Work', content: scope || `• Discovery & Planning Phase\n• UI/UX Design & Prototyping\n• Full-Stack Development\n• AI Integration & Automation\n• Testing & Quality Assurance\n• Deployment & Training\n• 30-Day Post-Launch Support` },
        { title: 'Timeline & Milestones', content: timeline || `• Week 1-2: Requirements & Design\n• Week 3-6: Core Development\n• Week 7: AI Features Integration\n• Week 8: Testing & Refinement\n• Week 9: Deployment & Launch` },
        { title: 'Investment', content: budget || `Total Investment: $8,500\n\n• 50% upon project kickoff\n• 25% upon mid-project review\n• 25% upon final delivery\n\nIncludes: Development, Design, AI Integration, 3 months support` },
        { title: 'Why Choose Us', content: `• AI-Powered Development: 10x faster delivery\n• Proven Track Record: 150+ successful projects\n• Dedicated Support: WhatsApp + Dashboard\n• Future-Proof: Scalable architecture with MCP integration` },
        { title: 'Next Steps', content: `1. Review and approve this proposal\n2. Sign agreement and make initial payment\n3. Schedule kickoff meeting\n4. Begin discovery phase\n\nWe are ready to start immediately upon approval.` },
      ]);
      setIsGenerating(false);
    }, 4000);
  };

  return (
    <div className="space-y-4">
      <Card>
        <CardHeader><CardTitle className="flex items-center gap-2"><Sparkles className="w-5 h-5 text-purple-500" />AI Proposal Generator</CardTitle></CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2"><Label>Client Name</Label><Input value={clientName} onChange={(e) => setClientName(e.target.value)} placeholder="Acme Corp" /></div>
            <div className="space-y-2"><Label>Project Type</Label>
              <Select onValueChange={setProjectType}>
                <SelectTrigger><SelectValue placeholder="Select type..." /></SelectTrigger>
                <SelectContent>
                  <SelectItem value="Web Application">Web Application</SelectItem>
                  <SelectItem value="Mobile App">Mobile App</SelectItem>
                  <SelectItem value="E-commerce Platform">E-commerce Platform</SelectItem>
                  <SelectItem value="SaaS Dashboard">SaaS Dashboard</SelectItem>
                  <SelectItem value="AI Integration">AI Integration</SelectItem>
                  <SelectItem value="Custom Software">Custom Software</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
          <div className="space-y-2"><Label>Custom Scope (optional)</Label><Textarea value={scope} onChange={(e) => setScope(e.target.value)} placeholder="Enter custom scope of work, or leave blank for AI-generated..." className="h-24" /></div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2"><Label>Budget (optional)</Label><Input value={budget} onChange={(e) => setBudget(e.target.value)} placeholder="$5,000" /></div>
            <div className="space-y-2"><Label>Timeline (optional)</Label><Input value={timeline} onChange={(e) => setTimeline(e.target.value)} placeholder="6 weeks" /></div>
          </div>
          <Button onClick={handleGenerate} disabled={isGenerating || !clientName || !projectType} className="w-full gap-2">
            {isGenerating ? <><Loader2 className="w-4 h-4 animate-spin" />Generating...</> : <><Sparkles className="w-4 h-4" />Generate Proposal</>}
          </Button>
        </CardContent>
      </Card>

      {proposal && (
        <Card className="border-2 border-blue-200">
          <CardHeader className="border-b bg-blue-50 flex flex-row items-center justify-between">
            <CardTitle className="flex items-center gap-2"><FileText className="w-5 h-5" />Professional Proposal</CardTitle>
            <Button variant="outline" size="sm" className="gap-2"><Download className="w-4 h-4" />Export PDF</Button>
          </CardHeader>
          <CardContent className="p-6 space-y-6">
            {proposal.map((section, idx) => (
              <div key={idx} className="space-y-2">
                <h3 className="text-lg font-bold text-blue-900 border-b pb-1">{section.title}</h3>
                <p className="text-sm text-gray-700 whitespace-pre-wrap leading-relaxed">{section.content}</p>
              </div>
            ))}
            <div className="pt-4 border-t flex justify-between items-center">
              <p className="text-xs text-gray-500">Generated by AI Product Studio • {new Date().toLocaleDateString()}</p>
              <Button>Send to Client</Button>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}

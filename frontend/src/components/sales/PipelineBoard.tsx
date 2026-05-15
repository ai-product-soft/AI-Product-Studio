
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { MoreHorizontal, Phone, Mail, MessageCircle, ArrowRight } from 'lucide-react';

interface Lead { id: number; name: string; company: string; service: string; value: string; nextAction: string; }

const stages = [
  { id: 'new', title: 'New Leads', color: 'bg-blue-100 border-blue-300', badge: 'bg-blue-500' },
  { id: 'contacted', title: 'Contacted', color: 'bg-yellow-100 border-yellow-300', badge: 'bg-yellow-500' },
  { id: 'qualified', title: 'Qualified', color: 'bg-purple-100 border-purple-300', badge: 'bg-purple-500' },
  { id: 'proposal', title: 'Proposal Sent', color: 'bg-orange-100 border-orange-300', badge: 'bg-orange-500' },
  { id: 'negotiation', title: 'Negotiation', color: 'bg-pink-100 border-pink-300', badge: 'bg-pink-500' },
  { id: 'closed', title: 'Closed Won', color: 'bg-green-100 border-green-300', badge: 'bg-green-500' },
];

const leads: Record<string, Lead[]> = {
  new: [{ id: 1, name: 'Sarah Johnson', company: 'TechStart Inc', service: 'Web App', value: '$8,500', nextAction: 'Send intro email' }],
  contacted: [{ id: 2, name: 'Mike Chen', company: 'RetailMax', service: 'E-commerce', value: '$15,000', nextAction: 'Schedule call' }],
  qualified: [{ id: 3, name: 'Lisa Park', company: 'HealthPlus', service: 'Mobile App', value: '$22,000', nextAction: 'Prepare proposal' }],
  proposal: [{ id: 4, name: 'David Kim', company: 'FinanceHub', service: 'SaaS Dashboard', value: '$35,000', nextAction: 'Follow up' }],
  negotiation: [{ id: 5, name: 'Emma Wilson', company: 'EduLearn', service: 'AI Integration', value: '$12,000', nextAction: 'Review terms' }],
  closed: [{ id: 6, name: 'James Brown', company: 'ShopLocal', service: 'Web App', value: '$9,500', nextAction: 'Kickoff meeting' }],
};

export function PipelineBoard() {
  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-bold">Sales Pipeline</h2>
        <div className="flex gap-2 text-sm text-gray-600">
          <span>Total Pipeline: $102,000</span>
          <span>•</span>
          <span>Win Rate: 34%</span>
          <span>•</span>
          <span>Avg Deal: $17,000</span>
        </div>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {stages.map((stage) => (
          <Card key={stage.id} className={`${stage.color} border-2`}>
            <CardHeader className="p-3 pb-2"><CardTitle className="text-sm flex items-center justify-between"><span>{stage.title}</span><Badge className={stage.badge}>{leads[stage.id]?.length || 0}</Badge></CardTitle></CardHeader>
            <CardContent className="p-3 pt-0 space-y-2">
              {leads[stage.id]?.map((lead) => (
                <Card key={lead.id} className="bg-white shadow-sm hover:shadow-md transition-shadow cursor-pointer">
                  <CardContent className="p-3 space-y-2">
                    <div className="flex items-center justify-between">
                      <p className="font-medium text-sm">{lead.name}</p>
                      <Button variant="ghost" size="icon" className="h-6 w-6"><MoreHorizontal className="w-3 h-3" /></Button>
                    </div>
                    <p className="text-xs text-gray-500">{lead.company}</p>
                    <Badge variant="outline" className="text-xs">{lead.service}</Badge>
                    <p className="text-sm font-bold text-green-600">{lead.value}</p>
                    <div className="flex items-center gap-1 text-xs text-gray-400">
                      <ArrowRight className="w-3 h-3" />
                      <span>{lead.nextAction}</span>
                    </div>
                    <div className="flex gap-1 pt-1">
                      <Button variant="ghost" size="icon" className="h-7 w-7"><Phone className="w-3 h-3" /></Button>
                      <Button variant="ghost" size="icon" className="h-7 w-7"><Mail className="w-3 h-3" /></Button>
                      <Button variant="ghost" size="icon" className="h-7 w-7"><MessageCircle className="w-3 h-3" /></Button>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}


import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Activity, GitPullRequest, MessageSquare, CreditCard, FileText, Bell } from 'lucide-react';

interface ActivityItem { id: number; type: string; title: string; description: string; time: string; icon: React.ReactNode; color: string; }

const activities: ActivityItem[] = [
  { id: 1, type: 'project', title: 'New Project Started', description: 'E-commerce Platform for Client X', time: '2 min ago', icon: <GitPullRequest className="w-4 h-4" />, color: 'bg-blue-100 text-blue-600' },
  { id: 2, type: 'lead', title: 'New Lead Captured', description: 'John Doe - Mobile App Development', time: '15 min ago', icon: <MessageSquare className="w-4 h-4" />, color: 'bg-purple-100 text-purple-600' },
  { id: 3, type: 'payment', title: 'Payment Received', description: '$3,500 - Invoice #INV-2024-001', time: '1 hour ago', icon: <CreditCard className="w-4 h-4" />, color: 'bg-green-100 text-green-600' },
  { id: 4, type: 'approval', title: 'Approval Required', description: 'Proposal for SaaS Dashboard needs review', time: '3 hours ago', icon: <FileText className="w-4 h-4" />, color: 'bg-orange-100 text-orange-600' },
  { id: 5, type: 'notification', title: 'WhatsApp Alert', description: 'Lead from Instagram responded to follow-up', time: '5 hours ago', icon: <Bell className="w-4 h-4" />, color: 'bg-pink-100 text-pink-600' },
];

export function ActivityFeed() {
  return (
    <Card className="h-[400px]">
      <CardHeader className="border-b"><CardTitle className="flex items-center gap-2"><Activity className="w-5 h-5" />Recent Activity</CardTitle></CardHeader>
      <CardContent className="p-4">
        <div className="space-y-4">
          {activities.map((item) => (
            <div key={item.id} className="flex gap-3 items-start p-3 rounded-lg hover:bg-gray-50 transition-colors cursor-pointer">
              <div className={`p-2 rounded-full ${item.color} flex-shrink-0 mt-1`}>{item.icon}</div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium">{item.title}</p>
                <p className="text-xs text-gray-500 mt-1">{item.description}</p>
                <p className="text-xs text-gray-400 mt-1">{item.time}</p>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}

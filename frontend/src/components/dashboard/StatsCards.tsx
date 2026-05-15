import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { TrendingUp, Users, DollarSign, FolderKanban, CheckCircle, Clock } from 'lucide-react';

interface StatItem { title: string; value: string; change: string; icon: React.ReactNode; color: string; }

export function StatsCards() {
  const stats: StatItem[] = [
    { title: 'Total Revenue', value: '$24,500', change: '+12%', icon: <DollarSign className="w-5 h-5" />, color: 'bg-green-100 text-green-600' },
    { title: 'Active Projects', value: '8', change: '+2', icon: <FolderKanban className="w-5 h-5" />, color: 'bg-blue-100 text-blue-600' },
    { title: 'New Leads', value: '34', change: '+8%', icon: <Users className="w-5 h-5" />, color: 'bg-purple-100 text-purple-600' },
    { title: 'Completed', value: '156', change: '+23', icon: <CheckCircle className="w-5 h-5" />, color: 'bg-emerald-100 text-emerald-600' },
    { title: 'Pending Approvals', value: '5', change: '-1', icon: <Clock className="w-5 h-5" />, color: 'bg-orange-100 text-orange-600' },
    { title: 'Conversion Rate', value: '28%', change: '+4%', icon: <TrendingUp className="w-5 h-5" />, color: 'bg-indigo-100 text-indigo-600' },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {stats.map((stat, idx) => (
        <Card key={idx} className="hover:shadow-md transition-shadow">
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-gray-600">{stat.title}</CardTitle>
            <div className={`p-2 rounded-lg ${stat.color}`}>{stat.icon}</div>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stat.value}</div>
            <p className={`text-xs mt-1 ${stat.change.startsWith('+') ? 'text-green-600' : 'text-red-600'}`}>{stat.change} from last month</p>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}

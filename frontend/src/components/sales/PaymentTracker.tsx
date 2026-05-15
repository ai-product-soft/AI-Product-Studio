import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { DollarSign, CreditCard, CheckCircle, Clock, AlertCircle, Download, Eye } from 'lucide-react';

interface Payment { id: string; client: string; project: string; amount: string; method: string; status: string; date: string; }

const payments: Payment[] = [
  { id: 'PAY-001', client: 'TechStart Inc', project: 'E-commerce Platform', amount: '$3,500', method: 'Stripe', status: 'completed', date: '2024-01-10' },
  { id: 'PAY-002', client: 'RetailMax', project: 'Inventory System', amount: '$2,000', method: 'Bank Transfer', status: 'pending', date: '2024-01-12' },
  { id: 'PAY-003', client: 'HealthPlus', project: 'Mobile App', amount: '$5,500', method: 'PayPal', status: 'completed', date: '2024-01-08' },
  { id: 'PAY-004', client: 'FinanceHub', project: 'SaaS Dashboard', amount: '$8,000', method: 'Stripe', status: 'processing', date: '2024-01-14' },
  { id: 'PAY-005', client: 'EduLearn', project: 'AI Tutor', amount: '$4,200', method: 'Crypto', status: 'completed', date: '2024-01-05' },
];

const statusConfig = {
  completed: { icon: <CheckCircle className="w-4 h-4" />, color: 'bg-green-100 text-green-700', label: 'Completed' },
  pending: { icon: <Clock className="w-4 h-4" />, color: 'bg-yellow-100 text-yellow-700', label: 'Pending' },
  processing: { icon: <AlertCircle className="w-4 h-4" />, color: 'bg-blue-100 text-blue-700', label: 'Processing' },
  failed: { icon: <AlertCircle className="w-4 h-4" />, color: 'bg-red-100 text-red-700', label: 'Failed' },
};

export function PaymentTracker() {
  return (
    <div className="space-y-4">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card><CardContent className="p-4 flex items-center gap-3"><div className="p-2 bg-green-100 rounded-lg"><DollarSign className="w-5 h-5 text-green-600" /></div><div><p className="text-sm text-gray-500">Total Revenue</p><p className="text-xl font-bold">$23,200</p></div></CardContent></Card>
        <Card><CardContent className="p-4 flex items-center gap-3"><div className="p-2 bg-blue-100 rounded-lg"><CreditCard className="w-5 h-5 text-blue-600" /></div><div><p className="text-sm text-gray-500">This Month</p><p className="text-xl font-bold">$8,500</p></div></CardContent></Card>
        <Card><CardContent className="p-4 flex items-center gap-3"><div className="p-2 bg-yellow-100 rounded-lg"><Clock className="w-5 h-5 text-yellow-600" /></div><div><p className="text-sm text-gray-500">Pending</p><p className="text-xl font-bold">$2,000</p></div></CardContent></Card>
        <Card><CardContent className="p-4 flex items-center gap-3"><div className="p-2 bg-purple-100 rounded-lg"><CheckCircle className="w-5 h-5 text-purple-600" /></div><div><p className="text-sm text-gray-500">Completed</p><p className="text-xl font-bold">18</p></div></CardContent></Card>
      </div>

      <Card>
        <CardHeader className="flex flex-row items-center justify-between"><CardTitle>Payment History</CardTitle><Button variant="outline" size="sm" className="gap-2"><Download className="w-4 h-4" />Export</Button></CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow><TableHead>ID</TableHead><TableHead>Client</TableHead><TableHead>Project</TableHead><TableHead>Amount</TableHead><TableHead>Method</TableHead><TableHead>Status</TableHead><TableHead>Date</TableHead><TableHead>Actions</TableHead></TableRow>
            </TableHeader>
            <TableBody>
              {payments.map((payment) => (
                <TableRow key={payment.id}>
                  <TableCell className="font-mono text-xs">{payment.id}</TableCell>
                  <TableCell className="font-medium">{payment.client}</TableCell>
                  <TableCell className="text-sm text-gray-600">{payment.project}</TableCell>
                  <TableCell className="font-bold">{payment.amount}</TableCell>
                  <TableCell><Badge variant="outline">{payment.method}</Badge></TableCell>
                  <TableCell><Badge className={statusConfig[payment.status as keyof typeof statusConfig].color}>{statusConfig[payment.status as keyof typeof statusConfig].icon}{statusConfig[payment.status as keyof typeof statusConfig].label}</Badge></TableCell>
                  <TableCell className="text-sm text-gray-500">{payment.date}</TableCell>
                  <TableCell><Button variant="ghost" size="icon" className="h-8 w-8"><Eye className="w-4 h-4" /></Button></TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
}


import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { CheckCircle2, XCircle, Trophy } from 'lucide-react';

interface Competitor { name: string; price: string; features: string[]; score: number; }

const competitors: Competitor[] = [
  { name: 'Your Product', price: '$99/mo', features: ['AI Integration', 'Custom Workflows', 'White-label', 'API Access', '24/7 Support'], score: 92 },
  { name: 'Competitor A', price: '$299/mo', features: ['AI Integration', 'Custom Workflows', 'White-label', 'API Access', 'Business Hours'], score: 78 },
  { name: 'Competitor B', price: '$149/mo', features: ['AI Integration', 'Templates', 'White-label', '-', 'Email Support'], score: 65 },
  { name: 'Competitor C', price: '$499/mo', features: ['AI Integration', 'Custom Workflows', 'White-label', 'API Access', '24/7 Support'], score: 85 },
];

const featureLabels = ['AI Integration', 'Custom Workflows', 'White-label', 'API Access', '24/7 Support'];

export function CompetitorMatrix() {
  return (
    <Card>
      <CardHeader><CardTitle className="flex items-center gap-2"><Trophy className="w-5 h-5 text-yellow-500" />Competitor Analysis Matrix</CardTitle></CardHeader>
      <CardContent>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead className="w-[180px]">Feature</TableHead>
              {competitors.map((c) => <TableHead key={c.name} className={c.name === 'Your Product' ? 'bg-blue-50 font-bold' : ''}>{c.name}</TableHead>)}
            </TableRow>
          </TableHeader>
          <TableBody>
            <TableRow><TableCell className="font-medium">Price</TableCell>{competitors.map((c) => <TableCell key={c.name} className={c.name === 'Your Product' ? 'bg-blue-50 font-bold text-green-600' : ''}>{c.price}</TableCell>)}</TableRow>
            {featureLabels.map((feature) => (
              <TableRow key={feature}>
                <TableCell className="font-medium">{feature}</TableCell>
                {competitors.map((c) => (
                  <TableCell key={c.name} className={c.name === 'Your Product' ? 'bg-blue-50' : ''}>
                    {c.features.includes(feature) ? <CheckCircle2 className="w-5 h-5 text-green-500" /> : <XCircle className="w-5 h-5 text-red-300" />}
                  </TableCell>
                ))}
              </TableRow>
            ))}
            <TableRow><TableCell className="font-medium">Score</TableCell>{competitors.map((c) => <TableCell key={c.name} className={c.name === 'Your Product' ? 'bg-blue-50 font-bold text-lg' : 'text-lg'}>{c.score}/100</TableCell>)}</TableRow>
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  );
}

import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Textarea } from '@/components/ui/textarea';
import { UserPlus, CheckCircle } from 'lucide-react';

const services = ['Web Application', 'Mobile App', 'AI Integration', 'E-commerce', 'SaaS Platform', 'Custom Software', 'Consulting'];
const budgets = ['Under $1,000', '$1,000 - $5,000', '$5,000 - $10,000', '$10,000 - $25,000', '$25,000+'];
const timelines = ['ASAP (1-2 weeks)', 'Standard (1-2 months)', 'Relaxed (3-6 months)', 'Long-term (6+ months)'];

export function LeadCaptureForm() {
  const [submitted, setSubmitted] = useState(false);
  const [formData, setFormData] = useState({ name: '', email: '', phone: '', company: '', service: '', budget: '', timeline: '', description: '', vision: '' });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitted(true);
    setTimeout(() => setSubmitted(false), 5000);
  };

  if (submitted) {
    return (
      <Card className="w-full max-w-2xl mx-auto">
        <CardContent className="flex flex-col items-center justify-center py-12 space-y-4">
          <CheckCircle className="w-16 h-16 text-green-500" />
          <h2 className="text-2xl font-bold text-center">Thank You!</h2>
          <p className="text-gray-600 text-center">We have received your request. Our team will contact you within 24 hours via WhatsApp and email.</p>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="w-full max-w-2xl mx-auto">
      <CardHeader><CardTitle className="flex items-center gap-2"><UserPlus className="w-5 h-5" />Project Inquiry</CardTitle></CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2"><Label htmlFor="name">Full Name *</Label><Input id="name" required value={formData.name} onChange={(e) => setFormData({...formData, name: e.target.value})} /></div>
            <div className="space-y-2"><Label htmlFor="email">Email *</Label><Input id="email" type="email" required value={formData.email} onChange={(e) => setFormData({...formData, email: e.target.value})} /></div>
            <div className="space-y-2"><Label htmlFor="phone">Phone (WhatsApp)</Label><Input id="phone" type="tel" value={formData.phone} onChange={(e) => setFormData({...formData, phone: e.target.value})} /></div>
            <div className="space-y-2"><Label htmlFor="company">Company</Label><Input id="company" value={formData.company} onChange={(e) => setFormData({...formData, company: e.target.value})} /></div>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="space-y-2"><Label>Service Needed</Label>
              <Select onValueChange={(v) => setFormData({...formData, service: v})}>
                <SelectTrigger><SelectValue placeholder="Select..." /></SelectTrigger>
                <SelectContent>{services.map((s) => <SelectItem key={s} value={s}>{s}</SelectItem>)}</SelectContent>
              </Select>
            </div>
            <div className="space-y-2"><Label>Budget Range</Label>
              <Select onValueChange={(v) => setFormData({...formData, budget: v})}>
                <SelectTrigger><SelectValue placeholder="Select..." /></SelectTrigger>
                <SelectContent>{budgets.map((b) => <SelectItem key={b} value={b}>{b}</SelectItem>)}</SelectContent>
              </Select>
            </div>
            <div className="space-y-2"><Label>Timeline</Label>
              <Select onValueChange={(v) => setFormData({...formData, timeline: v})}>
                <SelectTrigger><SelectValue placeholder="Select..." /></SelectTrigger>
                <SelectContent>{timelines.map((t) => <SelectItem key={t} value={t}>{t}</SelectItem>)}</SelectContent>
              </Select>
            </div>
          </div>
          <div className="space-y-2"><Label htmlFor="description">Project Description</Label><Textarea id="description" placeholder="Describe what you need..." className="h-24" value={formData.description} onChange={(e) => setFormData({...formData, description: e.target.value})} /></div>
          <div className="space-y-2"><Label htmlFor="vision">Your Vision</Label><Textarea id="vision" placeholder="What does success look like?" className="h-24" value={formData.vision} onChange={(e) => setFormData({...formData, vision: e.target.value})} /></div>
          <Button type="submit" className="w-full">Submit Inquiry</Button>
        </form>
      </CardContent>
    </Card>
  );
}

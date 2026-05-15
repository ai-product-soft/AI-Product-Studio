import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { MessageCircle, Send, CheckCheck, Clock } from 'lucide-react';

interface ChatMessage { id: number; sender: string; content: string; time: string; status: string; isMe: boolean; }

const chatHistory: ChatMessage[] = [
  { id: 1, sender: 'Sarah Johnson', content: 'Hi! I saw your portfolio. Can you build a custom CRM for my real estate business?', time: '10:30 AM', status: 'read', isMe: false },
  { id: 2, sender: 'You', content: 'Hello Sarah! Absolutely, we specialize in custom CRM solutions. What specific features do you need?', time: '10:32 AM', status: 'read', isMe: true },
  { id: 3, sender: 'Sarah Johnson', content: 'Lead tracking, automated follow-ups, and integration with property listing APIs.', time: '10:35 AM', status: 'read', isMe: false },
  { id: 4, sender: 'You', content: 'Perfect! That aligns well with our AI-powered lead management system. I will prepare a proposal for you.', time: '10:38 AM', status: 'delivered', isMe: true },
];

export function WhatsAppWidget() {
  const [newMessage, setNewMessage] = useState('');
  const [messages, setMessages] = useState(chatHistory);

  const handleSend = () => {
    if (!newMessage.trim()) return;
    const msg: ChatMessage = { id: messages.length + 1, sender: 'You', content: newMessage, time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }), status: 'sent', isMe: true };
    setMessages([...messages, msg]);
    setNewMessage('');
    setTimeout(() => {
      setMessages(prev => prev.map(m => m.id === msg.id ? {...m, status: 'delivered'} : m));
      setTimeout(() => {
        setMessages(prev => prev.map(m => m.id === msg.id ? {...m, status: 'read'} : m));
      }, 2000);
    }, 1500);
  };

  return (
    <Card className="w-full h-[500px] flex flex-col">
      <CardHeader className="border-b bg-green-50">
        <CardTitle className="flex items-center gap-2 text-sm">
          <div className="w-8 h-8 rounded-full bg-green-500 flex items-center justify-center"><MessageCircle className="w-4 h-4 text-white" /></div>
          <div className="flex-1">
            <p className="font-medium">WhatsApp Business</p>
            <p className="text-xs text-gray-500 flex items-center gap-1"><CheckCheck className="w-3 h-3 text-blue-500" />Connected • 5 active chats</p>
          </div>
          <Badge variant="outline" className="bg-green-100 text-green-700">Online</Badge>
        </CardTitle>
      </CardHeader>
      <CardContent className="flex-1 flex flex-col p-0">
        <div className="flex-1 overflow-y-auto p-4 space-y-3">
          {messages.map((msg) => (
            <div key={msg.id} className={`flex ${msg.isMe ? 'justify-end' : 'justify-start'}`}>
              <div className={`max-w-[80%] p-3 rounded-lg ${msg.isMe ? 'bg-green-100 text-green-900' : 'bg-gray-100 text-gray-800'}`}>
                <p className="text-sm">{msg.content}</p>
                <div className="flex items-center justify-end gap-1 mt-1">
                  <span className="text-xs text-gray-500">{msg.time}</span>
                  {msg.isMe && msg.status === 'read' && <CheckCheck className="w-3 h-3 text-blue-500" />}
                  {msg.isMe && msg.status === 'delivered' && <CheckCheck className="w-3 h-3 text-gray-400" />}
                  {msg.isMe && msg.status === 'sent' && <Clock className="w-3 h-3 text-gray-400" />}
                </div>
              </div>
            </div>
          ))}
        </div>
        <div className="p-3 border-t flex gap-2">
          <Input placeholder="Type a message..." value={newMessage} onChange={(e) => setNewMessage(e.target.value)} onKeyDown={(e) => e.key === 'Enter' && handleSend()} className="flex-1" />
          <Button size="icon" onClick={handleSend} className="bg-green-600 hover:bg-green-700"><Send className="w-4 h-4" /></Button>
        </div>
      </CardContent>
    </Card>
  );
}

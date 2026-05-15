import React, { useState, useRef, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Mic, Send, Bot, User, Loader2 } from 'lucide-react';

interface Message { role: 'user' | 'assistant'; content: string; timestamp: Date; }

export function MasterAIChatbox() {
  const [messages, setMessages] = useState<Message[]>([{ role: 'assistant', content: 'Hello! I am your AI Product Studio assistant. I can help you with:\n\n• Research & Analysis\n• Project Planning\n• Code Generation\n• Marketing Strategy\n• Lead Management\n\nWhat would you like to do today?', timestamp: new Date() }]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const messagesEndRef = useRef<<HTMLDivElement>(null);
  const scrollToBottom = () => messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  useEffect(() => scrollToBottom(), [messages]);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;
    const userMessage: Message = { role: 'user', content: input, timestamp: new Date() };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);
    setTimeout(() => {
      const responses: Record<string, string> = { 'research': 'I will start market research for your idea.', 'plan': 'I will create a detailed project plan.', 'code': 'I will generate the complete application code.', 'marketing': 'I will create ad campaigns and social posts.', 'lead': 'I will set up lead generation campaigns.', 'proposal': 'I will generate a professional proposal.', 'default': 'I understand. Let me process that and get back to you.' };
      const lowerInput = input.toLowerCase();
      let response = responses.default;
      for (const [key, value] of Object.entries(responses)) { if (lowerInput.includes(key)) { response = value; break; } }
      setMessages(prev => [...prev, { role: 'assistant', content: response, timestamp: new Date() }]);
      setIsLoading(false);
    }, 1500);
  };

  const handleVoice = () => {
    if (!('webkitSpeechRecognition' in window)) { alert('Voice input not supported. Please use Chrome.'); return; }
    const recognition = new (window as any).webkitSpeechRecognition();
    recognition.lang = 'en-US';
    recognition.onstart = () => setIsListening(true);
    recognition.onend = () => setIsListening(false);
    recognition.onresult = (event: any) => setInput(event.results[0][0].transcript);
    recognition.start();
  };

  return (
    <Card className="w-full h-[600px] flex flex-col">
      <CardHeader className="border-b"><CardTitle className="flex items-center gap-2"><Bot className="w-6 h-6 text-blue-500" />Master AI Command Center</CardTitle></CardHeader>
      <CardContent className="flex-1 flex flex-col p-4">
        <div className="flex-1 overflow-y-auto space-y-4 mb-4">
          {messages.map((msg, idx) => (
            <div key={idx} className={`flex gap-3 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              {msg.role === 'assistant' && <div className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center flex-shrink-0"><Bot className="w-5 h-5 text-blue-600" /></div>}
              <div className={`max-w-[80%] p-3 rounded-lg ${msg.role === 'user' ? 'bg-blue-500 text-white' : 'bg-gray-100 text-gray-800'}`}>
                <p className="text-sm whitespace-pre-wrap">{msg.content}</p>
                <span className="text-xs opacity-70 mt-1 block">{msg.timestamp.toLocaleTimeString()}</span>
              </div>
              {msg.role === 'user' && <div className="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center flex-shrink-0"><User className="w-5 h-5 text-white" /></div>}
            </div>
          ))}
          {isLoading && <div className="flex gap-3"><div className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center"><Loader2 className="w-5 h-5 text-blue-600 animate-spin" /></div><div className="bg-gray-100 p-3 rounded-lg"><p className="text-sm">Thinking...</p></div></div>}
          <div ref={messagesEndRef} />
        </div>
        <div className="flex gap-2">
          <Button variant="outline" size="icon" onClick={handleVoice} className={isListening ? 'bg-red-100 animate-pulse' : ''}><Mic className="w-4 h-4" /></Button>
          <Input value={input} onChange={(e) => setInput(e.target.value)} onKeyDown={(e) => e.key === 'Enter' && handleSend()} placeholder="Type your command..." className="flex-1" />
          <Button onClick={handleSend} disabled={isLoading}><Send className="w-4 h-4" /></Button>
        </div>
      </CardContent>
    </Card>
  );
}

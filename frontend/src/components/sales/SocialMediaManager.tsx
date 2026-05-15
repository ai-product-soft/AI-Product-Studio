import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Badge } from '@/components/ui/badge';
import { Calendar, Instagram, Linkedin, Twitter, Send, Sparkles, Image as ImageIcon } from 'lucide-react';

interface Post { id: number; platform: string; content: string; status: string; scheduledAt: string; engagement: string; }

const posts: Post[] = [
  { id: 1, platform: 'instagram', content: 'Just launched a new AI-powered e-commerce platform! 10x faster checkout, smart recommendations, and seamless inventory management.', status: 'published', scheduledAt: '2024-01-15 10:00', engagement: '234 likes • 45 comments' },
  { id: 2, platform: 'linkedin', content: 'Why every startup needs an AI integration strategy in 2024. Our latest case study shows 40% efficiency gains.', status: 'scheduled', scheduledAt: '2024-01-16 09:00', engagement: 'Pending' },
  { id: 3, platform: 'twitter', content: 'Tired of slow web apps? Our new performance optimization service guarantees fast load times. DM us for a free audit.', status: 'draft', scheduledAt: 'Not scheduled', engagement: '-' },
];

export function SocialMediaManager() {
  const [newPost, setNewPost] = useState('');
  const [selectedPlatform, setSelectedPlatform] = useState('instagram');

  const platformIcons = { instagram: <Instagram className="w-4 h-4" />, linkedin: <Linkedin className="w-4 h-4" />, twitter: <Twitter className="w-4 h-4" /> };
  const platformColors = { instagram: 'bg-pink-100 text-pink-600', linkedin: 'bg-blue-100 text-blue-600', twitter: 'bg-sky-100 text-sky-600' };

  return (
    <div className="space-y-4">
      <Card>
        <CardHeader><CardTitle className="flex items-center gap-2"><Sparkles className="w-5 h-5 text-purple-500" />AI Content Studio</CardTitle></CardHeader>
        <CardContent className="space-y-4">
          <Tabs defaultValue="create" className="w-full">
            <TabsList className="grid w-full grid-cols-3">
              <TabsTrigger value="create">Create Post</TabsTrigger>
              <TabsTrigger value="scheduled">Scheduled</TabsTrigger>
              <TabsTrigger value="published">Published</TabsTrigger>
            </TabsList>
            <TabsContent value="create" className="space-y-4">
              <div className="flex gap-2">
                {Object.entries(platformIcons).map(([platform, icon]) => (
                  <Button key={platform} variant={selectedPlatform === platform ? 'default' : 'outline'} size="sm" className="gap-2" onClick={() => setSelectedPlatform(platform)}>
                    {icon}{platform.charAt(0).toUpperCase() + platform.slice(1)}
                  </Button>
                ))}
              </div>
              <Textarea placeholder="What would you like to share? AI will optimize for engagement..." className="h-32" value={newPost} onChange={(e) => setNewPost(e.target.value)} />
              <div className="flex gap-2">
                <Button variant="outline" className="gap-2"><ImageIcon className="w-4 h-4" />Add Media</Button>
                <Button variant="outline" className="gap-2"><Calendar className="w-4 h-4" />Schedule</Button>
                <Button className="flex-1 gap-2"><Send className="w-4 h-4" />Post Now</Button>
              </div>
            </TabsContent>
            <TabsContent value="scheduled" className="space-y-3">
              {posts.filter(p => p.status === 'scheduled').map((post) => (
                <Card key={post.id} className="hover:shadow-md transition-shadow">
                  <CardContent className="p-4 flex items-start gap-3">
                    <div className={`p-2 rounded-full ${platformColors[post.platform as keyof typeof platformColors]}`}>{platformIcons[post.platform as keyof typeof platformIcons]}</div>
                    <div className="flex-1">
                      <p className="text-sm text-gray-700 line-clamp-2">{post.content}</p>
                      <div className="flex items-center gap-2 mt-2 text-xs text-gray-500"><Calendar className="w-3 h-3" />{post.scheduledAt}</div>
                    </div>
                    <Badge variant="outline">Scheduled</Badge>
                  </CardContent>
                </Card>
              ))}
            </TabsContent>
            <TabsContent value="published" className="space-y-3">
              {posts.filter(p => p.status === 'published').map((post) => (
                <Card key={post.id} className="hover:shadow-md transition-shadow">
                  <CardContent className="p-4 flex items-start gap-3">
                    <div className={`p-2 rounded-full ${platformColors[post.platform as keyof typeof platformColors]}`}>{platformIcons[post.platform as keyof typeof platformIcons]}</div>
                    <div className="flex-1">
                      <p className="text-sm text-gray-700 line-clamp-2">{post.content}</p>
                      <div className="flex items-center gap-2 mt-2 text-xs text-gray-500"><Calendar className="w-3 h-3" />{post.scheduledAt} • {post.engagement}</div>
                    </div>
                    <Badge className="bg-green-100 text-green-700">Published</Badge>
                  </CardContent>
                </Card>
              ))}
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>
    </div>
  );
}

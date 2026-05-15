import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { cn } from '@/lib/utils';
import { LayoutDashboard, BarChart3, Users, FileText, Settings, Bot, CreditCard, Megaphone, FolderKanban } from 'lucide-react';

const navItems = [
  { href: '/dashboard', label: 'Dashboard', icon: <LayoutDashboard className="w-5 h-5" /> },
  { href: '/analysis', label: 'Analysis', icon: <BarChart3 className="w-5 h-5" /> },
  { href: '/sales', label: 'Sales & Marketing', icon: <Megaphone className="w-5 h-5" /> },
  { href: '/projects', label: 'Projects', icon: <FolderKanban className="w-5 h-5" /> },
  { href: '/leads', label: 'Leads', icon: <Users className="w-5 h-5" /> },
  { href: '/proposals', label: 'Proposals', icon: <FileText className="w-5 h-5" /> },
  { href: '/payments', label: 'Payments', icon: <CreditCard className="w-5 h-5" /> },
  { href: '/settings', label: 'Settings', icon: <Settings className="w-5 h-5" /> },
];

export function Sidebar() {
  const pathname = usePathname();
  return (
    <div className="w-64 bg-white border-r flex flex-col">
      <div className="p-4 border-b">
        <div className="flex items-center gap-2">
          <Bot className="w-8 h-8 text-blue-600" />
          <div>
            <h1 className="font-bold text-lg">AI Product Studio</h1>
            <p className="text-xs text-gray-500">v4.0</p>
          </div>
        </div>
      </div>
      <nav className="flex-1 p-4 space-y-1">
        {navItems.map((item) => (
          <Link key={item.href} href={item.href} className={cn("flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors", pathname === item.href ? "bg-blue-50 text-blue-700" : "text-gray-600 hover:bg-gray-50 hover:text-gray-900")}>
            {item.icon}
            {item.label}
          </Link>
        ))}
      </nav>
      <div className="p-4 border-t">
        <div className="bg-blue-50 rounded-lg p-3">
          <p className="text-xs font-medium text-blue-900">AI Status</p>
          <p className="text-xs text-blue-600 mt-1">Gemini 2.5 Flash Active</p>
        </div>
      </div>
    </div>
  );
}

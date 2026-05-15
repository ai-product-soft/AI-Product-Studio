import { useEffect, useState, useCallback } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import {
  ArrowLeft,
  Loader2,
  Search,
  FileText,
  Code,
  Megaphone,
  CreditCard,
  Download,
  CheckCircle,
  XCircle,
  Clock,
} from 'lucide-react'
import {
  getProject,
  getJobs,
  startResearch,
  startPlan,
  startGeneration,
  startPromotion,
  startSales,
  getDownloadToken,
} from '@/services/api'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/tabs'
import { Alert, AlertTitle, AlertDescription } from '@/components/ui/alert'

interface Project {
  id: number
  name: string
  client_idea: string
  status: string
  created_at: string
  jobs: Job[]
  research_briefs: any[]
  project_plans: any[]
  ad_campaigns: any[]
  invoices: any[]
}

interface Job {
  id: number
  job_type: string
  status: string
  error: string | null
  created_at: string
}

const statusOrder = [
  'idea',
  'researching',
  'research_complete',
  'planning',
  'plan_complete',
  'generating',
  'generation_review',
  'promoting',
  'sales_ready',
  'completed',
]

const statusLabels: Record<string, string> = {
  idea: 'Idea',
  researching: 'Researching Market',
  research_complete: 'Research Complete',
  planning: 'Planning Architecture',
  plan_complete: 'Plan Complete',
  generating: 'Generating Code',
  generation_review: 'Code Review',
  promoting: 'Creating Ads & Content',
  sales_ready: 'Sales Ready',
  completed: 'Completed',
  failed: 'Failed',
}

export default function ProjectDetail() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [project, setProject] = useState<Project | null>(null)
  const [loading, setLoading] = useState(true)
  const [activeAction, setActiveAction] = useState<string | null>(null)

  const fetchProject = useCallback(async () => {
    if (!id) return
    try {
      const { data } = await getProject(Number(id))
      setProject(data)
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }, [id])

  useEffect(() => {
    fetchProject()
  }, [fetchProject])

  useEffect(() => {
    if (!id) return
    const interval = setInterval(async () => {
      try {
        const { data: jobs } = await getJobs(Number(id))
        setProject((prev) => (prev ? { ...prev, jobs } : prev))
        if (jobs.some((j: Job) => j.status === 'completed' || j.status === 'failed')) {
          fetchProject()
        }
      } catch (err) {
        // silent fail on polling
      }
    }, 5000)

    return () => clearInterval(interval)
  }, [id, fetchProject])

  const handleAction = async (action: string, apiCall: () => Promise<any>) => {
    setActiveAction(action)
    try {
      await apiCall()
      fetchProject()
    } catch (err) {
      alert(`Failed to start ${action}`)
    } finally {
      setActiveAction(null)
    }
  }

  const handleDownload = async () => {
    if (!id) return
    try {
      const { data } = await getDownloadToken(Number(id))
      window.open(`/api/v1/download/${data.token}`, '_blank')
    } catch (err) {
      alert('Failed to generate download link')
    }
  }

  const getStatusIndex = (status: string) => statusOrder.indexOf(status)
  const currentStatusIndex = getStatusIndex(project?.status || 'idea')

  const canResearch = currentStatusIndex >= getStatusIndex('idea')
  const canPlan = currentStatusIndex >= getStatusIndex('research_complete')
  const canGenerate = currentStatusIndex >= getStatusIndex('plan_complete')
  const canPromote = currentStatusIndex >= getStatusIndex('generation_review')
  const canSales = currentStatusIndex >= getStatusIndex('sales_ready')
  const canDownload = currentStatusIndex >= getStatusIndex('completed')

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
      </div>
    )
  }

  if (!project) {
    return <div className="text-center text-muted-foreground">Project not found</div>
  }

  const runningJob = project.jobs.find((j) => j.status === 'running')

  return (
    <div className="space-y-6">
      <Button variant="ghost" onClick={() => navigate('/')} className="pl-0">
        <ArrowLeft className="mr-2 h-4 w-4" />
        Back
      </Button>

      <div className="flex items-start justify-between">
        <div>
          <h2 className="text-3xl font-bold tracking-tight">{project.name}</h2>
          <p className="text-muted-foreground mt-1 max-w-2xl">{project.client_idea}</p>
        </div>
        <Badge variant="secondary" className="text-sm">
          {statusLabels[project.status] || project.status}
        </Badge>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Automation Pipeline</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap gap-3">
            <Button
              size="sm"
              onClick={() => handleAction('research', () => startResearch(project.id))}
              disabled={!canResearch || !!runningJob || activeAction === 'research'}
            >
              {activeAction === 'research' ? <Loader2 className="h-4 w-4 animate-spin" /> : <Search className="h-4 w-4 mr-1" />}
              Research
            </Button>

            <Button
              size="sm"
              onClick={() => handleAction('plan', () => startPlan(project.id))}
              disabled={!canPlan || !!runningJob || activeAction === 'plan'}
            >
              {activeAction === 'plan' ? <Loader2 className="h-4 w-4 animate-spin" /> : <FileText className="h-4 w-4 mr-1" />}
              Plan
            </Button>

            <Button
              size="sm"
              onClick={() => handleAction('generate', () => startGeneration(project.id))}
              disabled={!canGenerate || !!runningJob || activeAction === 'generate'}
            >
              {activeAction === 'generate' ? <Loader2 className="h-4 w-4 animate-spin" /> : <Code className="h-4 w-4 mr-1" />}
              Generate
            </Button>

            <Button
              size="sm"
              onClick={() => handleAction('promote', () => startPromotion(project.id))}
              disabled={!canPromote || !!runningJob || activeAction === 'promote'}
            >
              {activeAction === 'promote' ? <Loader2 className="h-4 w-4 animate-spin" /> : <Megaphone className="h-4 w-4 mr-1" />}
              Promote
            </Button>

            <Button
              size="sm"
              onClick={() => handleAction('sales', () => startSales(project.id))}
              disabled={!canSales || !!runningJob || activeAction === 'sales'}
            >
              {activeAction === 'sales' ? <Loader2 className="h-4 w-4 animate-spin" /> : <CreditCard className="h-4 w-4 mr-1" />}
              Sales
            </Button>

            <Button
              size="sm"
              variant="outline"
              onClick={handleDownload}
              disabled={!canDownload}
            >
              <Download className="h-4 w-4 mr-1" />
              Download ZIP
            </Button>
          </div>

          {runningJob && (
            <div className="mt-4 flex items-center gap-2 text-sm text-blue-600">
              <Loader2 className="h-4 w-4 animate-spin" />
              Running: {runningJob.job_type} (Job #{runningJob.id})
            </div>
          )}
        </CardContent>
      </Card>

      {project.jobs.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Job History</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              {project.jobs.map((job) => (
                <div
                  key={job.id}
                  className="flex items-center justify-between p-3 rounded-md border text-sm"
                >
                  <div className="flex items-center gap-2">
                    {job.status === 'completed' && <CheckCircle className="h-4 w-4 text-green-500" />}
                    {job.status === 'failed' && <XCircle className="h-4 w-4 text-red-500" />}
                    {job.status === 'running' && <Loader2 className="h-4 w-4 animate-spin text-blue-500" />}
                    {job.status === 'pending' && <Clock className="h-4 w-4 text-muted-foreground" />}
                    <span className="capitalize">{job.job_type}</span>
                  </div>
                  <div className="flex items-center gap-4">
                    <Badge variant="outline" className="text-xs capitalize">
                      {job.status}
                    </Badge>
                    <span className="text-xs text-muted-foreground">
                      {new Date(job.created_at).toLocaleString()}
                    </span>
                  </div>
                  {job.error && (
                    <div className="w-full mt-1 text-xs text-red-600 bg-red-50 p-2 rounded">
                      {job.error}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      <Tabs defaultValue="research">
        <TabsList>
          <TabsTrigger value="research">Research</TabsTrigger>
          <TabsTrigger value="plan">Plan</TabsTrigger>
          <TabsTrigger value="promotion">Promotion</TabsTrigger>
          <TabsTrigger value="sales">Sales</TabsTrigger>
        </TabsList>

        <TabsContent value="research" className="mt-4">
          {project.research_briefs.length > 0 ? (
            <div className="space-y-4">
              {project.research_briefs.map((brief) => (
                <Card key={brief.id}>
                  <CardContent className="pt-6 space-y-4">
                    <div>
                      <h4 className="font-semibold mb-1">Summary</h4>
                      <p className="text-sm text-muted-foreground">{brief.summary}</p>
                    </div>
                    <div>
                      <h4 className="font-semibold mb-1">Opportunity Score</h4>
                      <div className="flex items-center gap-2">
                        <div className="h-2 flex-1 bg-muted rounded-full overflow-hidden">
                          <div
                            className="h-full bg-primary"
                            style={{ width: `${brief.opportunity_score}%` }}
                          />
                        </div>
                        <span className="text-sm font-medium">{brief.opportunity_score}/100</span>
                      </div>
                    </div>
                    {brief.competitors && brief.competitors.length > 0 && (
                      <div>
                        <h4 className="font-semibold mb-2">Competitors</h4>
                        <div className="grid gap-2">
                          {brief.competitors.map((comp: any, i: number) => (
                            <div key={i} className="p-3 border rounded-md text-sm">
                              <div className="font-medium">{comp.name}</div>
                              <div className="text-muted-foreground text-xs">{comp.url}</div>
                              <div className="mt-1 grid grid-cols-2 gap-2 text-xs">
                                <div>
                                  <span className="text-green-600 font-medium">Strength:</span> {comp.strength}
                                </div>
                                <div>
                                  <span className="text-red-600 font-medium">Weakness:</span> {comp.weakness}
                                </div>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                    {brief.key_insights && brief.key_insights.length > 0 && (
                      <div>
                        <h4 className="font-semibold mb-1">Key Insights</h4>
                        <ul className="list-disc list-inside text-sm text-muted-foreground space-y-1">
                          {brief.key_insights.map((insight: string, i: number) => (
                            <li key={i}>{insight}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </CardContent>
                </Card>
              ))}
            </div>
          ) : (
            <Alert>
              <AlertTitle>No research yet</AlertTitle>
              <AlertDescription>Click the Research button to start market analysis.</AlertDescription>
            </Alert>
          )}
        </TabsContent>

        <TabsContent value="plan" className="mt-4">
          {project.project_plans.length > 0 ? (
            <div className="space-y-4">
              {project.project_plans.map((plan) => (
                <Card key={plan.id}>
                  <CardContent className="pt-6 space-y-4">
                    {plan.phases && (
                      <div>
                        <h4 className="font-semibold mb-2">Implementation Phases</h4>
                        <div className="space-y-3">
                          {plan.phases.map((phase: any, i: number) => (
                            <div key={i} className="border rounded-md p-3">
                              <div className="flex items-center justify-between mb-2">
                                <span className="font-medium text-sm">{phase.phase}</span>
                                <Badge variant="outline" className="text-xs">{phase.duration}</Badge>
                              </div>
                              <ul className="list-disc list-inside text-sm text-muted-foreground space-y-1">
                                {phase.tasks.map((task: string, j: number) => (
                                  <li key={j}>{task}</li>
                                ))}
                              </ul>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                    {plan.tech_stack && (
                      <div>
                        <h4 className="font-semibold mb-2">Tech Stack</h4>
                        <div className="grid grid-cols-2 gap-2 text-sm">
                          {Object.entries(plan.tech_stack).map(([key, value]) => (
                            <div key={key} className="flex justify-between border-b pb-1">
                              <span className="text-muted-foreground capitalize">{key}</span>
                              <span className="font-medium">{String(value)}</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                    {plan.monetization_strategy && (
                      <div>
                        <h4 className="font-semibold mb-1">Monetization Strategy</h4>
                        <p className="text-sm text-muted-foreground">{plan.monetization_strategy}</p>
                      </div>
                    )}
                  </CardContent>
                </Card>
              ))}
            </div>
          ) : (
            <Alert>
              <AlertTitle>No plan yet</AlertTitle>
              <AlertDescription>Complete research first, then click Plan to generate architecture.</AlertDescription>
            </Alert>
          )}
        </TabsContent>

        <TabsContent value="promotion" className="mt-4">
          {project.ad_campaigns.length > 0 ? (
            <div className="space-y-4">
              {project.ad_campaigns.map((campaign) => (
                <Card key={campaign.id}>
                  <CardHeader>
                    <CardTitle className="text-base capitalize">{campaign.platform} Ads</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <pre className="text-xs bg-muted p-3 rounded-md overflow-auto">
                      {JSON.stringify(campaign.ad_copy, null, 2)}
                    </pre>
                  </CardContent>
                </Card>
              ))}
            </div>
          ) : (
            <Alert>
              <AlertTitle>No promotion assets yet</AlertTitle>
              <AlertDescription>Click Promote to generate ad copies and content.</AlertDescription>
            </Alert>
          )}
        </TabsContent>

        <TabsContent value="sales" className="mt-4">
          {project.invoices.length > 0 ? (
            <div className="space-y-4">
              {project.invoices.map((invoice) => (
                <Card key={invoice.id}>
                  <CardContent className="pt-6 space-y-3">
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-muted-foreground">Amount</span>
                      <span className="font-semibold">${(invoice.amount / 100).toFixed(2)} {invoice.currency.toUpperCase()}</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-muted-foreground">Status</span>
                      <Badge variant={invoice.status === 'paid' ? 'default' : 'secondary'}>{invoice.status}</Badge>
                    </div>
                    {invoice.stripe_payment_link && (
                      <div className="pt-2">
                        <a
                          href={invoice.stripe_payment_link}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-sm text-blue-600 hover:underline"
                        >
                          Stripe Payment Link →
                        </a>
                      </div>
                    )}
                  </CardContent>
                </Card>
              ))}
            </div>
          ) : (
            <Alert>
              <AlertTitle>No sales data yet</AlertTitle>
              <AlertDescription>Click Sales to generate payment links and invoices.</AlertDescription>
            </Alert>
          )}
        </TabsContent>
      </Tabs>
    </div>
  )
}

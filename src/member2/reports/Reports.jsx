import React from 'react'
import Layout from '../../app/Layout'
import PageHeader from '../../components/ui/PageHeader'
import { BarChart2, FileText, TrendingUp, Download } from 'lucide-react'

const reports = [
  {
    title: 'Monthly Airfare Report',
    description: 'Comprehensive overview of airfare movements and index changes',
    period: 'August 2026',
    icon: FileText,
    color: 'bg-blue-100 text-primary-blue'
  },
  {
    title: 'Airfare Index Summary',
    description: 'Historical index analysis and trend interpretation',
    period: 'August 2026',
    icon: TrendingUp,
    color: 'bg-teal-100 text-airtn-teal'
  },
  {
    title: 'Route Performance Report',
    description: 'Route-level fare analysis and comparisons',
    period: 'August 2026',
    icon: BarChart2,
    color: 'bg-green-100 text-success-green'
  },
  {
    title: 'Airline Comparison Report',
    description: 'Competitive analysis of airlines in the market',
    period: 'August 2026',
    icon: FileText,
    color: 'bg-amber-100 text-warning-amber'
  }
]

export default function Reports(){
  return (
    <Layout>
      <PageHeader 
        title="Reports" 
        description="Generated reports and analytical insights for stakeholders."
      />

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {reports.map((report, idx) => {
          const Icon = report.icon
          return (
            <div key={idx} className="bg-white rounded-lg border border-border-light p-6 shadow-sm hover:shadow-md transition-shadow">
              <div className="flex items-start justify-between mb-3">
                <div className={`p-3 rounded-lg ${report.color}`}>
                  <Icon className="w-6 h-6" />
                </div>
              </div>
              <h3 className="text-lg font-semibold text-primary-text">{report.title}</h3>
              <p className="text-sm text-secondary-text mt-2">{report.description}</p>
              <div className="mt-4 pt-4 border-t border-border-light flex items-center justify-between">
                <span className="text-xs text-secondary-text font-medium">{report.period}</span>
                <div className="flex gap-2">
                  <button className="p-2 rounded-lg hover:bg-body-bg transition-colors text-secondary-text hover:text-primary-blue">
                    <FileText className="w-4 h-4" />
                  </button>
                  <button className="p-2 rounded-lg hover:bg-body-bg transition-colors text-secondary-text hover:text-primary-blue">
                    <Download className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </div>
          )
        })}
      </div>

      {/* Additional Info */}
      <div className="mt-8 bg-blue-50 rounded-lg border border-blue-200 p-6">
        <h3 className="text-base font-semibold text-primary-blue mb-3">Report Generation</h3>
        <p className="text-sm text-primary-text mb-3">
          All reports are generated automatically based on the latest data in the AIRTN system. Reports are updated daily and available for download in multiple formats.
        </p>
        <p className="text-xs text-secondary-text">
          For custom reports or additional analysis, please contact the AIRTN support team.
        </p>
      </div>
    </Layout>
  )
}

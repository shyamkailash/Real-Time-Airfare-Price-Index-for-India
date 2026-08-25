import React from 'react'
import Layout from '../../app/Layout'
import PageHeader from '../../components/ui/PageHeader'
import { PieChart, Pie, Cell, ResponsiveContainer, Legend } from 'recharts'

const routeWeights = [
  { name: 'Delhi Routes', value: 32 },
  { name: 'Mumbai Routes', value: 28 },
  { name: 'Bengaluru Routes', value: 20 },
  { name: 'Hyderabad Routes', value: 12 },
  { name: 'Others', value: 8 }
]

const colors = ['#1769E0', '#00BFA6', '#F59E0B', '#16A34A', '#64748B']

export default function Methodology(){
  return (
    <Layout>
      <PageHeader 
        title="Methodology" 
        description="Understand how the Airfare Price Index is constructed."
      />

      <div className="space-y-6">
        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column - 65% */}
          <div className="lg:col-span-2 space-y-6">
            {/* Key Methodology Details */}
            <div className="bg-white rounded-lg border border-border-light p-6 shadow-sm">
              <h3 className="text-base font-semibold text-primary-text mb-4">Key Methodology Details</h3>
              <div className="space-y-3 text-sm">
                <div className="grid grid-cols-2 gap-4">
                  <div className="py-3 border-b border-border-light">
                    <p className="text-secondary-text">Base Period</p>
                    <p className="font-medium text-primary-text mt-1">January 2025</p>
                  </div>
                  <div className="py-3 border-b border-border-light">
                    <p className="text-secondary-text">Route Basket</p>
                    <p className="font-medium text-primary-text mt-1">24 major domestic routes</p>
                  </div>
                  <div className="py-3 border-b border-border-light">
                    <p className="text-secondary-text">Data Sources</p>
                    <p className="font-medium text-primary-text mt-1">Airlines + OTAs</p>
                  </div>
                  <div className="py-3 border-b border-border-light">
                    <p className="text-secondary-text">Collection Frequency</p>
                    <p className="font-medium text-primary-text mt-1">Daily</p>
                  </div>
                  <div className="py-3">
                    <p className="text-secondary-text">Price Measure</p>
                    <p className="font-medium text-primary-text mt-1">Fare per flight</p>
                  </div>
                  <div className="py-3">
                    <p className="text-secondary-text">Missing Data Handling</p>
                    <p className="font-medium text-primary-text mt-1">Carried forward</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Data Quality */}
            <div className="bg-white rounded-lg border border-border-light p-6 shadow-sm">
              <h3 className="text-base font-semibold text-primary-text mb-4">Data Quality Metrics</h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {[
                  { label: 'Data Coverage', value: '98.4%' },
                  { label: 'Accuracy Rate', value: '99.1%' },
                  { label: 'Timeliness', value: '< 5 min' },
                  { label: 'Consistency', value: '98.7%' }
                ].map((metric, idx) => (
                  <div key={idx} className="p-4 bg-body-bg rounded-lg text-center">
                    <p className="text-xs text-secondary-text">{metric.label}</p>
                    <p className="text-2xl font-bold text-primary-blue mt-2">{metric.value}</p>
                  </div>
                ))}
              </div>
              <p className="text-xs text-secondary-text mt-4 italic">Note: These are demonstration metrics for the prototype</p>
            </div>
          </div>

          {/* Right Column - 35% */}
          <div className="space-y-6">
            {/* Route Weight Distribution */}
            <div className="bg-white rounded-lg border border-border-light p-6 shadow-sm">
              <h3 className="text-base font-semibold text-primary-text mb-4">Route Weight Distribution</h3>
              <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={routeWeights}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ name, value }) => `${name} ${value}%`}
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="value"
                    >
                      {routeWeights.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={colors[index % colors.length]} />
                      ))}
                    </Pie>
                  </PieChart>
                </ResponsiveContainer>
              </div>
              <p className="text-xs text-secondary-text mt-4 italic text-center">Illustrative prototype weights</p>
            </div>

            {/* Note */}
            <div className="bg-blue-50 rounded-lg border border-blue-200 p-4">
              <h4 className="text-sm font-semibold text-primary-blue mb-2">Prototype Methodology</h4>
              <p className="text-xs text-primary-text leading-relaxed">
                This methodology documentation is for demonstration purposes. Official AIRTN methodology is subject to review and approval by relevant statistical agencies.
              </p>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  )
}

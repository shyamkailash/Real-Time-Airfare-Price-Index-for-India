import React from 'react'
import Layout from '../app/Layout'
import { Link } from 'react-router-dom'
import { XCircle, ArrowLeft } from 'lucide-react'

export default function NotFound(){
  return (
    <Layout>
      <div className="flex items-center justify-center min-h-96 px-4">
        <div className="bg-white rounded-lg border border-border-light p-8 md:p-12 max-w-md w-full text-center shadow-sm">
          <div className="flex justify-center mb-6">
            <div className="p-3 bg-warning-amber/10 rounded-lg">
              <XCircle className="w-12 h-12 text-warning-amber" />
            </div>
          </div>

          <div className="mb-3">
            <div className="text-6xl font-extrabold text-warning-amber mb-2">404</div>
          </div>

          <h1 className="text-2xl font-semibold text-primary-text mb-2">Page Not Found</h1>
          <p className="text-sm text-secondary-text mb-6">
            Sorry — the page you are looking for doesn't exist or has been moved. Check the URL or return to the dashboard.
          </p>

          <Link 
            to="/" 
            className="inline-flex items-center justify-center gap-2 px-6 py-2 bg-primary-blue text-white rounded-lg font-medium hover:bg-bright-blue transition-colors"
          >
            <ArrowLeft className="w-4 h-4" />
            Back to Overview
          </Link>
        </div>
      </div>
    </Layout>
  )
}

import { useState } from 'react';
import { User, CheckCircle, Info } from 'lucide-react';
import RequestModal from '../components/RequestModal';

export default function Settings({ user, setUser }) {
  const [modalOpen, setModalOpen] = useState(false);

  return (
    <div className="space-y-8 pb-20">
      
      <RequestModal 
        isOpen={modalOpen} 
        onClose={() => setModalOpen(false)}
        title="Request Profile Update"
        type="profile_update"
        defaultDetails="I would like to update my profile information..."
      />

      {/* Two Column Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Left Sidebar */}
        <div className="space-y-6">
          
          {/* Avatar & Name Card */}
          <div className="bg-white rounded-xl p-8 border border-slate-100 text-center">
            {/* Avatar */}
            <div className="w-32 h-32 mx-auto mb-6 rounded-full bg-gradient-to-br from-orange-200 to-orange-300 flex items-center justify-center overflow-hidden">
              <div className="w-full h-full bg-gradient-to-b from-transparent to-orange-400/20 flex items-center justify-center">
                <User size={48} className="text-slate-700" />
              </div>
            </div>

            {/* Name & Enrollment */}
            <h2 className="text-2xl font-black text-slate-900 mb-1">{user.name || 'Alex Thompson'}</h2>
            <p className="text-slate-500 font-medium mb-6">ENR-{user.enrollment_no || '2024-12345'}</p>

            {/* Edit Profile Button */}
            <button 
              onClick={() => setModalOpen(true)}
              className="w-full py-3 bg-blue-500 hover:bg-blue-600 text-white font-bold rounded-lg transition-all active:scale-[0.98] shadow-md shadow-blue-500/20"
            >
              Edit Profile
            </button>
          </div>

          {/* Library Status Card */}
          <div className="bg-white rounded-xl p-6 border border-slate-100">
            <h3 className="text-lg font-bold text-slate-900 mb-4">Library Status</h3>
            
            <div className="space-y-3">
              {/* Active Membership Badge */}
              <div className="flex items-center gap-3 px-4 py-3 bg-green-50 rounded-lg border border-green-100">
                <div className="w-8 h-8 rounded-full bg-green-100 flex items-center justify-center shrink-0">
                  <CheckCircle className="text-green-600" size={18} />
                </div>
                <span className="text-sm font-bold text-green-700">Active Membership</span>
              </div>

              {/* No Outstanding Fines Badge */}
              <div className="flex items-center gap-3 px-4 py-3 bg-blue-50 rounded-lg border border-blue-100">
                <div className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center shrink-0">
                  <Info className="text-blue-600" size={18} />
                </div>
                <span className="text-sm font-bold text-blue-700">No Outstanding Fines</span>
              </div>
            </div>
          </div>

        </div>

        {/* Right Column - Main Content */}
        <div className="lg:col-span-2 space-y-6">

          {/* Academic Information */}
          <div className="bg-white rounded-xl p-8 border border-slate-100">
            <h2 className="text-2xl font-bold text-slate-900 mb-6">Academic Information</h2>
            
            <div className="space-y-6">
              <InfoRow label="Department" value={user.department || 'Computer Science'} />
              <InfoRow label="Year of Study" value={`${user.year || '3rd'} Year`} />
              <InfoRow label="Email Address" value={user.email || `${user.name?.toLowerCase().replace(' ', '.')}@university.edu`} />
            </div>
          </div>

          {/* Borrowing Privileges */}
          <div className="bg-white rounded-xl p-8 border border-slate-100">
            <h2 className="text-2xl font-bold text-slate-900 mb-6">Borrowing Privileges</h2>
            
            <div className="space-y-6">
              <InfoRow label="Max Books Allowed" value="5 Books" />
              <InfoRow label="Loan Duration" value="21 Days" />
              <InfoRow label="Renewal Limits" value="2 Renewals per book" />
            </div>
          </div>

          {/* Account & Security */}
          <div className="bg-white rounded-xl p-8 border border-slate-100">
            <h2 className="text-2xl font-bold text-slate-900 mb-6">Account & Security</h2>
            
            <div className="flex items-center justify-between py-4 border-b border-slate-100">
              <div>
                <p className="font-bold text-slate-900 mb-1">Password</p>
                <p className="text-sm text-slate-500">Last changed on 12th Jan 2024</p>
              </div>
              <button 
                onClick={() => alert('Password change coming soon! Please contact admin.')}
                className="px-6 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold rounded-lg transition-colors"
              >
                Change Password
              </button>
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}

function InfoRow({ label, value }) {
  return (
    <div className="flex items-center justify-between py-3 border-b border-slate-100 last:border-0">
      <span className="text-slate-600 font-medium">{label}</span>
      <span className="text-slate-900 font-bold">{value}</span>
    </div>
  );
}

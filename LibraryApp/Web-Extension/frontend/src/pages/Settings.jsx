import { useState } from 'react';
import axios from 'axios';

export default function Settings({ user, setUser }) {
  // Local state for settings form
  const [email, setEmail] = useState(user?.email || 'alex.thompson@university.edu');
  const [libraryAlerts, setLibraryAlerts] = useState(false);
  const [loanReminders, setLoanReminders] = useState(true);
  const [darkMode, setDarkMode] = useState(false);
  const [language, setLanguage] = useState('English');
  const [dataConsent, setDataConsent] = useState(true);

  // Password Change State
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [isChangingPassword, setIsChangingPassword] = useState(false);
  const [isSavingPassword, setIsSavingPassword] = useState(false);
  const [passwordMsg, setPasswordMsg] = useState('');

  const handleChangePassword = async () => {
    if (newPassword.length < 4) {
        setPasswordMsg('Password must be at least 4 characters');
        return;
    }
    if (newPassword !== confirmPassword) {
        setPasswordMsg('Passwords do not match');
        return;
    }

    setIsSavingPassword(true);
    setPasswordMsg('');

    try {
        const { data } = await axios.post('/api/change-password', { new_password: newPassword });
        if (data.status === 'success') {
            setPasswordMsg('Success! Password updated.');
            // Refresh to update auth state and clear alerts
            setTimeout(() => window.location.reload(), 1000);
        } else {
            setPasswordMsg(data.message || 'Failed to update');
        }
    } catch (e) {
        setPasswordMsg(e.response?.data?.message || 'Server error');
    } finally {
        setIsSavingPassword(false);
    }
  };

  const handleSave = () => {
    // Determine the user's name to use in the alert
    const userName = user?.name ? user.name.split(' ')[0] : 'User';
    alert(`Changes saved successfully for ${userName}!`);
  };

  // Initial State Tracking
  const initialSettings = {
    email: user?.email || 'alex.thompson@university.edu',
    libraryAlerts: false,
    loanReminders: true,
    darkMode: false,
    language: 'English',
    dataConsent: true
  };

  const isDirty = 
    email !== initialSettings.email ||
    libraryAlerts !== initialSettings.libraryAlerts ||
    loanReminders !== initialSettings.loanReminders ||
    darkMode !== initialSettings.darkMode ||
    language !== initialSettings.language ||
    dataConsent !== initialSettings.dataConsent;

  return (
    <div className="max-w-4xl mx-auto pb-20">
      
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-slate-900">Settings</h1>
        <p className="text-slate-500 mt-1">Manage your account, application, and privacy settings.</p>
      </div>

      <div className="space-y-6">
        
        {/* Account Settings Card */}
        <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-6 md:p-8">
          <h2 className="text-xl font-bold text-slate-900 mb-6">Account Settings</h2>
          
          <div className="space-y-8">
            
            {/* Email Address */}
            <div className="grid md:grid-cols-3 gap-4 items-start">
              <div className="md:col-span-1">
                <label className="block font-bold text-slate-900 mb-1">Email Address</label>
                <p className="text-sm text-slate-500">Update the email address associated with your account.</p>
              </div>
              <div className="md:col-span-2">
                <input 
                  type="email" 
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all text-slate-900"
                />
              </div>
            </div>

            {/* Password */}
            <div className="grid md:grid-cols-3 gap-4 items-start">
              <div className="md:col-span-1">
                <label className="block font-bold text-slate-900 mb-1">Password</label>
                <p className="text-sm text-slate-500">Set a new password for your account.</p>
              </div>
              <div className="md:col-span-2 space-y-3">
                {!isChangingPassword ? (
                   <button 
                     onClick={() => setIsChangingPassword(true)}
                     className="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-900 font-bold rounded-lg transition-colors border border-slate-200"
                   >
                     Change Password
                   </button>
                ) : (
                  <div className="bg-slate-50 p-4 rounded-xl border border-slate-200 space-y-4 animate-fade-in">
                     <div>
                       <label className="block text-sm font-semibold text-slate-700 mb-1">New Password</label>
                       <input 
                         type="password"
                         value={newPassword}
                         onChange={(e) => setNewPassword(e.target.value)}
                         className="w-full px-3 py-2 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-500 outline-none bg-white"
                         placeholder="Min 4 characters"
                       />
                     </div>
                     <div>
                       <label className="block text-sm font-semibold text-slate-700 mb-1">Confirm Password</label>
                       <input 
                         type="password"
                         value={confirmPassword}
                         onChange={(e) => setConfirmPassword(e.target.value)}
                         className="w-full px-3 py-2 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-500 outline-none bg-white"
                         placeholder="Re-enter password"
                       />
                     </div>
                     <div className="flex items-center gap-2 pt-2">
                        <button 
                          onClick={handleChangePassword}
                          disabled={isSavingPassword}
                          className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-lg text-sm transition-colors"
                        >
                          {isSavingPassword ? 'Updating...' : 'Update Password'}
                        </button>
                        <button 
                          onClick={() => {
                            setIsChangingPassword(false);
                            setNewPassword('');
                            setConfirmPassword('');
                            setPasswordMsg('');
                          }}
                          className="px-4 py-2 text-slate-600 hover:bg-slate-200 font-bold rounded-lg text-sm transition-colors"
                        >
                          Cancel
                        </button>
                     </div>
                     {passwordMsg && (
                       <p className={`text-sm font-medium ${passwordMsg.includes('Success') ? 'text-green-600' : 'text-red-500'}`}>
                         {passwordMsg}
                       </p>
                     )}
                  </div>
                )}
              </div>
            </div>

            {/* Notification Preferences */}
            <div className="grid md:grid-cols-3 gap-4 items-start border-t border-slate-100 pt-8">
              <div className="md:col-span-1">
                <label className="block font-bold text-slate-900 mb-1">Notification Preferences</label>
                <p className="text-sm text-slate-500">Choose which notifications you want to receive.</p>
              </div>
              <div className="md:col-span-2 space-y-4">
                
                <div className="flex items-center justify-between">
                  <span className="text-slate-700 font-medium">Library Alerts</span>
                  <Switch checked={libraryAlerts} onChange={setLibraryAlerts} />
                </div>

                <div className="flex items-center justify-between">
                  <span className="text-slate-700 font-medium">Loan Reminders</span>
                  <Switch checked={loanReminders} onChange={setLoanReminders} />
                </div>

              </div>
            </div>

          </div>
        </div>

        {/* Application Preferences Card */}
        <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-6 md:p-8">
          <h2 className="text-xl font-bold text-slate-900 mb-6">Application Preferences</h2>
          
          <div className="space-y-8">
            
            {/* Theme */}
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div>
                <label className="block font-bold text-slate-900 mb-1">Theme</label>
                <p className="text-sm text-slate-500">Switch between light and dark mode.</p>
              </div>
              <div className="flex items-center gap-3">
                <span className="text-slate-700 font-medium">{darkMode ? 'Dark Mode' : 'Light Mode'}</span>
                <Switch checked={darkMode} onChange={setDarkMode} />
              </div>
            </div>

            {/* Light separator */}
            <div className="border-t border-slate-100"></div>

            {/* Language */}
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div>
                <label className="block font-bold text-slate-900 mb-1">Language</label>
                <p className="text-sm text-slate-500">Select your preferred language.</p>
              </div>
              <div className="w-full md:w-64">
                <select 
                  value={language}
                  onChange={(e) => setLanguage(e.target.value)}
                  className="w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all text-slate-900 bg-white cursor-pointer"
                >
                  <option>English</option>
                  <option>Spanish</option>
                  <option>French</option>
                  <option>German</option>
                </select>
              </div>
            </div>

          </div>
        </div>

        {/* Privacy Settings Card */}
        <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-6 md:p-8">
          <h2 className="text-xl font-bold text-slate-900 mb-6">Privacy Settings</h2>
          
          <div className="space-y-8">
            
            {/* Data Usage */}
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div className="flex-1">
                <label className="block font-bold text-slate-900 mb-1">Data Usage Consent</label>
                <p className="text-sm text-slate-500 mb-1">Allow us to use your data to improve our services.</p>
                <a href="#" className="text-brand-blue hover:text-blue-700 text-sm font-medium">Learn more</a>
              </div>
              <div>
                <Switch checked={dataConsent} onChange={setDataConsent} />
              </div>
            </div>

            {/* Light separator */}
            <div className="border-t border-slate-100"></div>

            {/* Delete Account */}
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div>
                <label className="block font-bold text-slate-900 mb-1">Delete Account</label>
                <p className="text-sm text-slate-500">Permanently delete your account and all associated data.</p>
              </div>
              <div>
                <button 
                  onClick={() => alert('Account deletion requested. Admin will be notified.')}
                  className="px-4 py-2.5 bg-red-600 hover:bg-red-700 text-white font-bold rounded-lg transition-colors shadow-sm"
                >
                  Request Data Deletion
                </button>
              </div>
            </div>

          </div>
        </div>

      </div>

      {/* Footer Actions - Only show if changes made */}
      {isDirty && (
        <div className="mt-8 flex items-center justify-end gap-3 bg-slate-50 p-4 rounded-xl animate-fade-in fixed bottom-6 right-6 md:static md:bg-transparent md:p-0">
            <button 
            className="px-6 py-2.5 bg-white hover:bg-slate-100 text-slate-700 font-bold rounded-lg border border-slate-200 transition-colors shadow-sm md:shadow-none"
            onClick={() => {
                // Reset state
                setEmail(initialSettings.email);
                setLibraryAlerts(initialSettings.libraryAlerts);
                setLoanReminders(initialSettings.loanReminders);
                setDarkMode(initialSettings.darkMode);
                setLanguage(initialSettings.language);
                setDataConsent(initialSettings.dataConsent);
            }}
            >
            Cancel
            </button>
            <button 
            className="px-6 py-2.5 bg-brand-blue hover:bg-blue-600 text-white font-bold rounded-lg shadow-sm transition-all active:scale-[0.98]"
            onClick={handleSave}
            >
            Save Changes
            </button>
        </div>
      )}
    </div>
  );
}

// Custom Switch Component
function Switch({ checked, onChange }) {
  return (
    <button 
      role="switch"
      aria-checked={checked}
      onClick={() => onChange(!checked)}
      className={`
        relative inline-flex h-7 w-12 shrink-0 cursor-pointer rounded-full border-2 border-transparent 
        transition-colors duration-200 ease-in-out focus:outline-none focus-visible:ring-2 
        focus-visible:ring-brand-blue focus-visible:ring-offset-2
        ${checked ? 'bg-brand-blue' : 'bg-slate-200'}
      `}
    >
      <span className="sr-only">Use setting</span>
      <span
        aria-hidden="true"
        className={`
          pointer-events-none inline-block h-6 w-6 transform rounded-full bg-white shadow ring-0 
          transition duration-200 ease-in-out
          ${checked ? 'translate-x-5' : 'translate-x-0'}
        `}
      />
    </button>
  );
}

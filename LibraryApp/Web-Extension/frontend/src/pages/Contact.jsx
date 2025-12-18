import { Mail, Linkedin, HeartHandshake, Github } from 'lucide-react';

export default function Contact() {
  return (
    <div className="min-h-screen bg-slate-50/50 dark:bg-slate-950 pb-24 md:pb-10 transition-colors flex items-center justify-center px-4">
      <div className="max-w-5xl w-full bg-white dark:bg-slate-900 rounded-3xl shadow-lg border border-slate-200/60 dark:border-slate-800/80 p-8 md:p-12 space-y-10">
        <header className="space-y-3 text-center">
          <div className="inline-flex items-center justify-center rounded-2xl bg-blue-50 dark:bg-blue-900/20 px-5 py-3 text-blue-700 dark:text-blue-300 text-base font-bold mb-3">
            <HeartHandshake className="w-5 h-5 mr-2" />
            Contact Us
          </div>
          <h1 className="text-3xl md:text-4xl font-black tracking-tight text-slate-900 dark:text-white">
            GPA Library Portal Support
          </h1>
          <p className="text-slate-600 dark:text-slate-400 text-base md:text-lg">
            Found a bug, need help, or want to suggest a new feature? Reach out to the team below.
          </p>
        </header>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* Yash Date */}
          <div className="rounded-2xl border border-slate-200 dark:border-slate-800 bg-slate-50/60 dark:bg-slate-900/60 p-7 space-y-4">
            <p className="text-sm font-semibold uppercase tracking-wide text-slate-400 dark:text-slate-500">
              Developer & Maintainer
            </p>
            <h2 className="text-xl font-bold text-slate-900 dark:text-white">Yash Vijay Date</h2>
            <p className="text-sm text-slate-500 dark:text-slate-400">
              Primary contact for GPA Library Portal support and updates.
            </p>
            <div className="space-y-3 text-base">
              <a
                href="mailto:yashdate31@gmail.com"
                className="flex items-center gap-3 text-blue-600 dark:text-blue-400 hover:underline break-all"
              >
                <Mail className="w-5 h-5" />
                yashdate31@gmail.com
              </a>
              <a
                href="https://www.linkedin.com/in/yash-date-a361a8329/"
                target="_blank"
                rel="noreferrer"
                className="flex items-center gap-3 text-blue-600 dark:text-blue-400 hover:underline break-all"
              >
                <Linkedin className="w-5 h-5" />
                linkedin.com/in/yash-date-a361a8329/
              </a>
              <a
                href="https://github.com/yashdate"
                target="_blank"
                rel="noreferrer"
                className="flex items-center gap-3 text-blue-600 dark:text-blue-400 hover:underline break-all"
              >
                <Github className="w-5 h-5" />
                github.com/yashdate
              </a>
            </div>
          </div>

          {/* Special Thanks - Yash Magar */}
          <div className="rounded-2xl border border-amber-200/80 dark:border-amber-800/80 bg-amber-50/70 dark:bg-amber-900/20 p-7 space-y-4">
            <p className="text-sm font-semibold uppercase tracking-wide text-amber-500 dark:text-amber-400">
              Special Thanks
            </p>
            <h2 className="text-xl font-bold text-slate-900 dark:text-white">Yash Magar</h2>
            <p className="text-sm text-slate-600 dark:text-slate-400">
              For valuable help and contributions to the portal.
            </p>
            <div className="space-y-3 text-base">
              <a
                href="mailto:yashajaymagar01@gmail.com"
                className="flex items-center gap-3 text-blue-700 dark:text-blue-300 hover:underline break-all"
              >
                <Mail className="w-5 h-5" />
                yashajaymagar01@gmail.com
              </a>
              <a
                href="https://www.linkedin.com/in/yash-magar-55a184395/"
                target="_blank"
                rel="noreferrer"
                className="flex items-center gap-3 text-blue-700 dark:text-blue-300 hover:underline break-all"
              >
                <Linkedin className="w-5 h-5" />
                linkedin.com/in/yash-magar-55a184395/
              </a>
            </div>
          </div>
        </div>

        <footer className="pt-4 border-t border-slate-100 dark:border-slate-800 text-center text-sm text-slate-500 dark:text-slate-500">
          Built for GPA Library – students first.
        </footer>
      </div>
    </div>
  );
}

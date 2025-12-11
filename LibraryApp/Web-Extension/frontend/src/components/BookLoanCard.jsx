import PropTypes from 'prop-types';
import { Calendar, AlertCircle, BookOpen, ExternalLink, RefreshCw } from 'lucide-react';
import Card from './ui/Card';
import Button from './ui/Button';

const BookLoanCard = ({ 
  title, 
  author, 
  dueDate, 
  status = 'normal', 
  fine, 
  onRenew, 
  onViewDetails,
  className = ''
}) => {
  
  // Status Configurations
  const statusConfig = {
    normal: {
      label: 'On Time',
      chipClass: 'bg-slate-100 text-slate-700 border-slate-200',
      icon: BookOpen
    },
    due_soon: {
      label: 'Due Soon',
      chipClass: 'bg-amber-50 text-amber-700 border-amber-200',
      icon: Calendar
    },
    overdue: {
      label: 'Overdue',
      chipClass: 'bg-red-50 text-red-700 border-red-200',
      icon: AlertCircle
    }
  };

  const currentConfig = statusConfig[status] || statusConfig.normal;
  const StatusIcon = currentConfig.icon;

  return (
    <Card className={`flex flex-col h-full transition-shadow hover:shadow-md ${className}`}>
      
      {/* Header: Status Chip */}
      <div className="flex justify-between items-start mb-3">
        <div className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold border ${currentConfig.chipClass}`}>
          <StatusIcon size={12} />
          {currentConfig.label}
        </div>
        
        {/* Fine Display if Overdue */}
        {status === 'overdue' && fine && (
          <div className="text-red-600 font-bold text-sm bg-red-50 px-2 py-1 rounded-md border border-red-100">
             {fine} Fine
          </div>
        )}
      </div>

      {/* Content */}
      <div className="flex-1 mb-4">
        <h3 className="text-lg font-bold text-slate-900 dark:text-white leading-tight mb-1 line-clamp-2 transition-colors" title={title}>
          {title}
        </h3>
        <p className="text-sm text-slate-500 dark:text-slate-400 font-medium mb-3 line-clamp-1 transition-colors">{author}</p>
        
        <div className="flex items-center gap-2 text-sm text-slate-600 dark:text-slate-300 bg-slate-50 dark:bg-slate-800/50 p-2 rounded-lg border border-slate-100 dark:border-slate-700 transition-colors">
           <Calendar size={14} className="text-slate-400 dark:text-slate-500" />
           <span className="font-medium">Due: {dueDate}</span>
        </div>
      </div>

      {/* Actions */}
      <div className="mt-auto grid grid-cols-2 gap-2">
         {onRenew && status !== 'overdue' && (
           <Button 
             variant="secondary" 
             size="sm" 
             leftIcon={<RefreshCw size={14} />}
             onClick={onRenew}
             className="w-full justify-center"
           >
             Renew
           </Button>
         )}
         
         <Button 
           variant={status === 'overdue' ? 'danger' : 'primary'} 
           size="sm"
           leftIcon={<ExternalLink size={14} />}
           onClick={onViewDetails}
           className={`w-full justify-center ${!onRenew || status === 'overdue' ? 'col-span-2' : ''}`}
         >
           Details
         </Button>
      </div>

    </Card>
  );
};

BookLoanCard.propTypes = {
  title: PropTypes.string.isRequired,
  author: PropTypes.string.isRequired,
  dueDate: PropTypes.string.isRequired,
  status: PropTypes.oneOf(['normal', 'due_soon', 'overdue']),
  fine: PropTypes.string,
  onRenew: PropTypes.func,
  onViewDetails: PropTypes.func,
  className: PropTypes.string
};

export default BookLoanCard;

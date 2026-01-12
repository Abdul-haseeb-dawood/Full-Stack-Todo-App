import React, { ReactNode } from 'react';

interface GlassCardProps {
  children: ReactNode;
  className?: string;
  onClick?: () => void;
}

const GlassCard: React.FC<GlassCardProps> = ({ children, className = '', onClick }) => {
  return (
    <div 
      className={`
        relative rounded-2xl border border-white/20 bg-white/10 backdrop-blur-md
        shadow-glass hover:shadow-lg transition-all duration-300 ease-in-out
        ${onClick ? 'cursor-pointer hover:scale-105' : ''}
        ${className}
      `}
      onClick={onClick}
    >
      <div className="p-6">
        {children}
      </div>
    </div>
  );
};

export default GlassCard;
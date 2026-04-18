const Card = ({ title, subtitle, children, className = '' }) => {
  return (
    <section className={`glass-card rounded-2xl p-5 ${className}`}>
      {(title || subtitle) && (
        <header className="mb-4">
          {title && <h3 className="text-lg font-semibold text-white">{title}</h3>}
          {subtitle && <p className="mt-1 text-sm text-slate-400">{subtitle}</p>}
        </header>
      )}
      {children}
    </section>
  );
};

export default Card;

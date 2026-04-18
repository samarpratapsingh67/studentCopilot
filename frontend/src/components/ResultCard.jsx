import Card from './Card';

const toneMap = {
  High: {
    text: 'text-rose-300',
    bar: 'bg-rose-500',
    badge: 'bg-rose-500/20 text-rose-300 border-rose-500/30',
  },
  Medium: {
    text: 'text-amber-300',
    bar: 'bg-amber-500',
    badge: 'bg-amber-500/20 text-amber-300 border-amber-500/30',
  },
  Low: {
    text: 'text-emerald-300',
    bar: 'bg-emerald-500',
    badge: 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30',
  },
};

const ResultCard = ({ result }) => {
  if (!result) {
    return (
      <Card title="Prediction Result" subtitle="Run a prediction to see churn insights." className="h-full">
        <div className="flex h-full min-h-48 items-center justify-center rounded-xl border border-dashed border-slate-700 bg-slate-900/30 p-6 text-center text-slate-400">
          Your churn score and segment breakdown will appear here.
        </div>
      </Card>
    );
  }

  const probabilityPct = Math.round(result.probability * 100);
  const segment = result.segment || 'Low';
  const tone = toneMap[segment] || toneMap.Low;
  const predictionLabel = result.churned === 1 ? 'Likely to Churn' : 'Likely to Stay';

  return (
    <Card title="Prediction Result" subtitle="Model response based on submitted customer profile." className="h-full">
      <div className="space-y-5">
        <div className="flex items-center justify-between">
          <p className="text-sm text-slate-400">Prediction</p>
          <span className="rounded-full border border-slate-700 px-3 py-1 text-xs font-medium text-slate-200">
            {result.status || 'Success'}
          </span>
        </div>

        <div className="rounded-xl border border-slate-700/80 bg-slate-900/60 p-4">
          <p className="text-sm text-slate-400">Outcome</p>
          <p className={`mt-1 text-xl font-semibold ${tone.text}`}>{predictionLabel}</p>
        </div>

        <div className="space-y-2">
          <div className="flex items-center justify-between text-sm text-slate-300">
            <span>Churn Probability</span>
            <span className="font-semibold text-white">{probabilityPct}%</span>
          </div>
          <div className="h-3 rounded-full bg-slate-800">
            <div
              className={`h-3 rounded-full transition-all duration-500 ${tone.bar}`}
              style={{ width: `${probabilityPct}%` }}
            />
          </div>
        </div>

        <div className="rounded-xl border border-slate-700/80 bg-slate-900/60 p-4">
          <p className="text-sm text-slate-400">Risk Segment</p>
          <span
            className={`mt-2 inline-flex rounded-full border px-3 py-1 text-sm font-semibold ${tone.badge}`}
          >
            {segment} Risk
          </span>
        </div>
      </div>
    </Card>
  );
};

export default ResultCard;

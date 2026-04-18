import { useEffect, useMemo, useState } from 'react';
import Card from '../components/Card';
import { fetchModelComparison } from '../services/api';

const formatPct = (value) => `${(Number(value || 0) * 100).toFixed(2)}%`;

const Dashboard = ({ onGoPredict }) => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [comparison, setComparison] = useState([]);
  const [bestModel, setBestModel] = useState('');

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      setError('');
      try {
        const data = await fetchModelComparison();
        setComparison(Array.isArray(data?.results) ? data.results : []);
        setBestModel(data?.best_model || '');
      } catch (err) {
        setError(err?.response?.data?.error || err?.message || 'Failed to load model comparison data.');
      } finally {
        setLoading(false);
      }
    };

    load();
  }, []);

  const bestModelMetrics = useMemo(
    () => comparison.find((item) => item.model === bestModel),
    [comparison, bestModel],
  );

  return (
    <section className="space-y-6">
      <div className="glass-card animate-fadeUp rounded-2xl p-6">
        <p className="text-sm uppercase tracking-[0.22em] text-orange-300">Model leaderboard</p>
        <h2 className="mt-2 text-2xl font-semibold text-white sm:text-3xl">Compare churn models on real test data.</h2>
        <p className="mt-3 max-w-3xl text-slate-300">
          Metrics below are computed from your Netflix churn dataset split and model setup from training.
          Best model is highlighted by F1 Score.
        </p>
        <button type="button" className="primary-btn mt-5" onClick={onGoPredict}>
          Score a Customer
        </button>
      </div>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-3">
        <Card className="animate-fadeUp" title="Models Compared">
          <p className="text-3xl font-semibold text-white">{comparison.length}</p>
          <p className="mt-2 text-sm text-slate-400">Total baseline models evaluated</p>
        </Card>

        <Card className="animate-fadeUp" title="Best Model">
          <p className="text-2xl font-semibold text-emerald-300">{bestModel || '-'}</p>
          <p className="mt-2 text-sm text-slate-400">Chosen by highest F1 Score</p>
        </Card>

        <Card className="animate-fadeUp" title="Best F1 Score">
          <p className="text-3xl font-semibold text-white">
            {bestModelMetrics ? formatPct(bestModelMetrics.f1_score) : '-'}
          </p>
          <p className="mt-2 text-sm text-slate-400">On held-out test data</p>
        </Card>
      </div>

      <Card title="Model Comparison" subtitle="Accuracy and F1 Score for each trained model.">
        {loading ? (
          <div className="rounded-xl border border-slate-700/80 bg-slate-900/50 p-5 text-sm text-slate-300">
            Loading comparison metrics...
          </div>
        ) : error ? (
          <div className="rounded-xl border border-rose-500/40 bg-rose-950/20 p-5 text-sm text-rose-200">{error}</div>
        ) : (
          <div className="overflow-x-auto rounded-xl border border-slate-700/80">
            <table className="min-w-full bg-slate-900/40 text-left text-sm">
              <thead className="bg-slate-800/70 text-slate-300">
                <tr>
                  <th className="px-4 py-3 font-medium">Model</th>
                  <th className="px-4 py-3 font-medium">Accuracy</th>
                  <th className="px-4 py-3 font-medium">F1 Score</th>
                  <th className="px-4 py-3 font-medium">Best</th>
                </tr>
              </thead>
              <tbody>
                {comparison.map((item) => {
                  const isBest = item.model === bestModel;
                  return (
                    <tr
                      key={item.model}
                      className={`border-t border-slate-800 text-slate-200 ${isBest ? 'bg-emerald-500/10' : ''}`}
                    >
                      <td className="px-4 py-3 font-medium text-white">{item.model}</td>
                      <td className="px-4 py-3">{formatPct(item.accuracy)}</td>
                      <td className="px-4 py-3">{formatPct(item.f1_score)}</td>
                      <td className="px-4 py-3">
                        {isBest ? (
                          <span className="rounded-full border border-emerald-400/40 bg-emerald-500/20 px-2 py-1 text-xs font-semibold text-emerald-300">
                            Best Model
                          </span>
                        ) : (
                          <span className="text-slate-500">-</span>
                        )}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </Card>
    </section>
  );
};

export default Dashboard;

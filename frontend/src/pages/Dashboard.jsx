import Card from '../components/Card';

const hardcodedComparison = [
  { model: 'CatBoosting Regressor', score: 0.979186 },
  { model: 'XGBRegressor', score: 0.978628 },
  { model: 'Random Forest Regressor', score: 0.977311 },
  { model: 'K-Neighbors Regressor', score: 0.972114 },
  { model: 'Decision Tree', score: 0.956741 },
  { model: 'Linear Regression', score: 0.937298 },
  { model: 'Ridge', score: 0.937297 },
  { model: 'Lasso', score: 0.937264 },
  { model: 'AdaBoost Regressor', score: 0.867945 },
];

const formatScore = (value) => Number(value || 0).toFixed(6);

const Dashboard = ({ onGoPredict }) => {
  const comparison = hardcodedComparison;
  const bestModel = comparison[0]?.model || '-';
  const bestModelScore = comparison[0]?.score;

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
          <p className="mt-2 text-sm text-slate-400">Chosen by highest score from provided list</p>
        </Card>

        <Card className="animate-fadeUp" title="Best Score">
          <p className="text-3xl font-semibold text-white">{bestModelScore !== undefined ? formatScore(bestModelScore) : '-'}</p>
          <p className="mt-2 text-sm text-slate-400">Top score in provided ranking</p>
        </Card>
      </div>

      <Card title="Model Comparison" subtitle="Hardcoded scores for provided models.">
        <div className="overflow-x-auto rounded-xl border border-slate-700/80">
          <table className="min-w-full bg-slate-900/40 text-left text-sm">
            <thead className="bg-slate-800/70 text-slate-300">
              <tr>
                <th className="px-4 py-3 font-medium">Model</th>
                <th className="px-4 py-3 font-medium">Score</th>
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
                    <td className="px-4 py-3">{formatScore(item.score)}</td>
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
      </Card>
    </section>
  );
};

export default Dashboard;

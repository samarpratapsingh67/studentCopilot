import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';
import Card from '../components/Card';

const summaryCards = [
  { title: 'Customers Scored', value: '12,480', note: '+8.6% vs last month' },
  { title: 'High Risk Accounts', value: '2,196', note: '17.6% of active base' },
  { title: 'Retention Lift', value: '11.9%', note: 'Estimated post-campaign' },
  { title: 'Avg Churn Probability', value: '34.7%', note: 'Across latest batch' },
];

const riskDistribution = [
  { name: 'Low', value: 58, color: '#22c55e' },
  { name: 'Medium', value: 25, color: '#f59e0b' },
  { name: 'High', value: 17, color: '#ef4444' },
];

const regionRisk = [
  { region: 'France', churnRate: 19 },
  { region: 'Germany', churnRate: 31 },
  { region: 'Spain', churnRate: 14 },
];

const Dashboard = ({ onGoPredict }) => {
  return (
    <section className="space-y-6">
      <div className="glass-card animate-fadeUp rounded-2xl p-6">
        <p className="text-sm uppercase tracking-[0.22em] text-orange-300">Retention command center</p>
        <h2 className="mt-2 text-2xl font-semibold text-white sm:text-3xl">
          Detect churn early and prioritize the right accounts.
        </h2>
        <p className="mt-3 max-w-3xl text-slate-300">
          This dashboard gives a quick read on current churn exposure. Switch to the prediction tab to score
          individual customers in real time.
        </p>
        <button type="button" className="primary-btn mt-5" onClick={onGoPredict}>
          Score a Customer
        </button>
      </div>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {summaryCards.map((item, index) => (
          <Card key={item.title} className="animate-fadeUp" title={item.title}>
            <p className="text-3xl font-semibold text-white">{item.value}</p>
            <p className="mt-2 text-sm text-slate-400">{item.note}</p>
            <p className="mt-3 text-xs text-slate-500">Card #{index + 1}</p>
          </Card>
        ))}
      </div>

      <div className="grid grid-cols-1 gap-4 xl:grid-cols-2">
        <Card title="Risk Distribution" subtitle="Current customer segmentation by churn probability.">
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={riskDistribution} dataKey="value" nameKey="name" innerRadius={70} outerRadius={110}>
                  {riskDistribution.map((entry) => (
                    <Cell key={entry.name} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={{
                    borderRadius: 12,
                    borderColor: '#334155',
                    background: '#0f172a',
                  }}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </Card>

        <Card title="Regional Churn Rate" subtitle="Estimated churn rate by country.">
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={regionRisk} margin={{ top: 16, right: 20, left: -10, bottom: 10 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="region" stroke="#94a3b8" />
                <YAxis stroke="#94a3b8" unit="%" />
                <Tooltip
                  contentStyle={{
                    borderRadius: 12,
                    borderColor: '#334155',
                    background: '#0f172a',
                  }}
                />
                <Bar dataKey="churnRate" fill="#f97316" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Card>
      </div>
    </section>
  );
};

export default Dashboard;

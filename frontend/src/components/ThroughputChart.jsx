import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts'
import { useInView } from '../hooks/useInView.js'

export default function ThroughputChart({ data }) {
  const [ref, isInView] = useInView({ threshold: 0.3 })

  return (
    <div ref={ref} className={`chart-panel ${isInView ? 'reveal--visible' : 'reveal'}`}>
      <div className="chart-panel__title">Processing Throughput (Events/sec)</div>
      <ResponsiveContainer width="100%" height={240}>
        <BarChart data={isInView ? data : []}>
          <CartesianGrid stroke="#262f4d" strokeDasharray="3 3" />
          <XAxis dataKey="time" stroke="#8991b8" fontSize={12} />
          <YAxis stroke="#8991b8" fontSize={12} />
          <Tooltip
            contentStyle={{
              background: '#1b2440',
              border: '1px solid #262f4d',
              borderRadius: 8,
              color: '#eef1fb',
            }}
          />
          <Bar
            dataKey="eventsPerSec"
            fill="#a78bfa"
            radius={[4, 4, 0, 0]}
            isAnimationActive={true}
            animationDuration={900}
            animationEasing="ease-out"
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
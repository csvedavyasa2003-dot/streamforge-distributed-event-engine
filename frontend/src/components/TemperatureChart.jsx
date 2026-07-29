import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts'
import { useInView } from '../hooks/useInView.js'

export default function TemperatureChart({ data }) {
  const [ref, isInView] = useInView({ threshold: 0.3 })

  return (
    <div ref={ref} className={`chart-panel ${isInView ? 'reveal--visible' : 'reveal'}`}>
      <div className="chart-panel__title">Average Temperature (Live Window)</div>
      <ResponsiveContainer width="100%" height={240}>
        <LineChart data={isInView ? data : []}>
          <CartesianGrid stroke="#232c3a" strokeDasharray="3 3" />
          <XAxis dataKey="time" stroke="#8a97a8" fontSize={12} />
          <YAxis stroke="#8a97a8" fontSize={12} unit="°C" />
          <Tooltip
            contentStyle={{
              background: '#1a2230',
              border: '1px solid #232c3a',
              borderRadius: 8,
              color: '#e6ebf1',
            }}
          />
          <Line
            type="monotone"
            dataKey="avgTemp"
            stroke="#3ddc97"
            strokeWidth={2}
            dot={false}
            isAnimationActive={true}
            animationDuration={1200}
            animationEasing="ease-out"
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
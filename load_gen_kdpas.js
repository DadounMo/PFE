import { sleep } from 'k6'
import http from 'k6/http'
import { htmlReport } from "https://raw.githubusercontent.com/benc-uk/k6-reporter/main/dist/bundle.js";

export const options = {
  ext: {
    loadimpact: {
      distribution: { 'amazon:us:ashburn': { loadZone: 'amazon:us:ashburn', percent: 100 } },
      apm: [],
    },
  },
  thresholds: {},
  scenarios: {
    Scenario_1: {
      executor: 'ramping-vus',
      gracefulStop: '30s',
      stages: [
		{ target:  180 , duration: '5m' },
		{ target:  201 , duration: '5m' },
		{ target:  204 , duration: '5m' },
		{ target:  188 , duration: '5m' },
		{ target:  235 , duration: '5m' },
		{ target:  227 , duration: '5m' },
		{ target:  234 , duration: '5m' },
		{ target:  264 , duration: '5m' },
		{ target:  302 , duration: '5m' },
		{ target:  293 , duration: '5m' },
		{ target:  259 , duration: '5m' },
		{ target:  229 , duration: '5m' },
		{ target:  203 , duration: '5m' },
		{ target:  229 , duration: '5m' },
		{ target:  242 , duration: '5m' },
		{ target:  233 , duration: '5m' },
		{ target:  267 , duration: '5m' },
		{ target:  269 , duration: '5m' },
		{ target:  270 , duration: '5m' },
		{ target:  315 , duration: '5m' },
		{ target:  364 , duration: '5m' },
		{ target:  347 , duration: '5m' },
		{ target:  312 , duration: '5m' },
		{ target:  274 , duration: '5m' },
		{ target:  237 , duration: '5m' },
		{ target:  278 , duration: '5m' },
		{ target:  284 , duration: '5m' },
		{ target:  277 , duration: '5m' },
		{ target:  317 , duration: '5m' },
		{ target:  313 , duration: '5m' },
		{ target:  318 , duration: '5m' },
		{ target:  374 , duration: '5m' },
		{ target:  413 , duration: '5m' },
		{ target:  405 , duration: '5m' },
		{ target:  355 , duration: '5m' },
		{ target:  306 , duration: '5m' },
		{ target:  271 , duration: '5m' },
		{ target:  306 , duration: '5m' },
		{ target:  315 , duration: '5m' },
		{ target:  301 , duration: '5m' },
		{ target:  356 , duration: '5m' },
		{ target:  348 , duration: '5m' },
      ],
      gracefulRampDown: '5m',
      exec: 'scenario_1',
    },
  },
}

export function handleSummary(data) {
  return {
    "/src/summary.html": htmlReport(data),
  };
}


export function scenario_1() {
  let response

  // FIB
  response = http.get('http://10.10.1.2:19634/fib/1000')

  // Automatically added sleep
  sleep(1)
}

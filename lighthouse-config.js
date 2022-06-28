const DEVTOOLS_RTT_ADJUSTMENT_FACTOR = 3.75;
const DEVTOOLS_THROUGHPUT_ADJUSTMENT_FACTOR = 0.9;

const throttling = {
  // These values align with WebPageTest's definition of "Fast 3G"
  // But offer similar charateristics to roughly the 75th percentile of 4G connections.
  // label="3G Fast (1.6 Mbps/768 Kbps 150ms RTT)"
  mobileSlow4G: {
    rttMs: 150,
    throughputKbps: 1.6 * 1024,
    requestLatencyMs: 150 * DEVTOOLS_RTT_ADJUSTMENT_FACTOR,
    downloadThroughputKbps: 1.6 * 1024 * DEVTOOLS_THROUGHPUT_ADJUSTMENT_FACTOR,
    uploadThroughputKbps: 750 * DEVTOOLS_THROUGHPUT_ADJUSTMENT_FACTOR,
    cpuSlowdownMultiplier: 2,
  },
  // These values partially align with WebPageTest's definition of "Regular 3G".
  // These values are meant to roughly align with Chrome UX report's 3G definition which are based
  // on HTTP RTT of 300-1400ms and downlink throughput of <700kbps.
  // label="3G (1.6 Mbps/768 Kbps 300ms RTT)"
  mobileRegular3G: {
    rttMs: 300,
    throughputKbps: 700,
    requestLatencyMs: 300 * DEVTOOLS_RTT_ADJUSTMENT_FACTOR,
    downloadThroughputKbps: 700 * DEVTOOLS_THROUGHPUT_ADJUSTMENT_FACTOR,
    uploadThroughputKbps: 700 * DEVTOOLS_THROUGHPUT_ADJUSTMENT_FACTOR,
    cpuSlowdownMultiplier: 4,
  },
  //[4G] label="4G (9 Mbps, 170ms RTT)"
  mobile4G: {
    rttMs: 170,
    downloadThroughputKbps: 900 * DEVTOOLS_THROUGHPUT_ADJUSTMENT_FACTOR,
    uploadThroughputKbps: 900 * DEVTOOLS_THROUGHPUT_ADJUSTMENT_FACTOR,
    cpuSlowdownMultiplier: 2,
  },
  //label="LTE (12 Mbps, 70ms RTT)"
  mobileLTE: {
    rttMs: 70,
    downloadThroughputKbps: 12000 * DEVTOOLS_THROUGHPUT_ADJUSTMENT_FACTOR,
    uploadThroughputKbps: 12000 * DEVTOOLS_THROUGHPUT_ADJUSTMENT_FACTOR,
    cpuSlowdownMultiplier: 2,
  },
  // Using a "broadband" connection type
  // Corresponds to "Dense 4G 25th percentile" in https://docs.google.com/document/d/1Ft1Bnq9-t4jK5egLSOc28IL4TvR-Tt0se_1faTA4KTY/edit#heading=h.bb7nfy2x9e5v
  desktopDense4G: {
    rttMs: 40,
    throughputKbps: 10 * 1024,
    cpuSlowdownMultiplier: 1,
    requestLatencyMs: 0, // 0 means unset
    downloadThroughputKbps: 0,
    uploadThroughputKbps: 0,
  },
};

const DESKTOP_EMULATION_METRICS = {
  // Macbook air
  mobile: false,
  width: 1280,
  height: 800,
  deviceScaleFactor: 1,
  disabled: false,
};

const IPHONE11_EMULATION_METRICS = {
  mobile: true,
  width: 414,
  height: 896,
  deviceScaleFactor: 2.625,
  disabled: false,
};

const screenEmulationMetrics = {
  mobile: IPHONE11_EMULATION_METRICS,
  desktop: DESKTOP_EMULATION_METRICS,
};

const IPHONE11_USERAGENT = 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A356 Safari/604.1 Chrome-Lighthouse';
const DESKTOP_USERAGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4695.0 Safari/537.36 Chrome-Lighthouse'; 

const userAgents = {
  mobile: IPHONE11_USERAGENT,
  desktop: DESKTOP_USERAGENT,
};

const userAgent = {
  defaultUserAgent:
    "Mozilla/5.0 (Linux; Android 7.0; Moto G (4)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4420.0 Mobile Safari/537.36 Chrome-Lighthouse",
  iPhoneUserAgent:
    "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A356 Safari/604.1 Chrome-Lighthouse",
};

const cpuSettings = {
  highEndDesktop_cpuSlowdownMultiplier: 1,
  lowEndDesktop_cpuSlowdownMultiplier: 2,
  highEndMobile_cpuSlowdownMultiplier: 2,
  midTierEndMobile_cpuSlowdownMultiplier: 4,
  lowEndMobile_cpuSlowdownMultiplier: 10,
};


// mobile configuration
 module.exports = {
   extends: "lighthouse:default",
   settings: {
     maxWaitForFcp: 30 * 1000,
     maxWaitForLoad: 45 * 1000,
     formFactor: 'mobile',
     disableStorageReset: false,
     throttlingMethod: "simulate",
     screenEmulation: screenEmulationMetrics.mobile,
     emulatedUserAgent: userAgents.mobile,
     throttling: throttling.mobileSlow4G,
     auditMode: false,
     gatherMode: false,
   },
 };

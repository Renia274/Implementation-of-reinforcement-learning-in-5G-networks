

#include "ns3/core-module.h"
#include "ns3/config-store.h"
#include "ns3/network-module.h"
#include "ns3/internet-module.h"
#include "ns3/internet-apps-module.h"
#include "ns3/applications-module.h"
#include "ns3/log.h"
#include "ns3/point-to-point-helper.h"
#include "ns3/flow-monitor-module.h"
#include "ns3/nr-helper.h"
#include "ns3/nr-point-to-point-epc-helper.h"
#include "ns3/ipv4-global-routing-helper.h"
#include "ns3/config-store-module.h"
#include "ns3/nr-mac-scheduler-tdma-rr.h"
#include "ns3/nr-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/ideal-beamforming-algorithm.h"
#include "ns3/config-store.h"
#include "ns3/eps-bearer-tag.h"
#include "ns3/abort.h"
#include "ns3/object.h"
#include "ns3/nr-mac-scheduler-ns3.h"
#include "ns3/nr-phy-mac-common.h"
#include "ns3/basic-data-calculators.h"
#include "ns3/nr-spectrum-phy.h"
#include "ns3/nr-ue-net-device.h"
#include <ns3/nr-ue-phy.h>
#include "ns3/nr-module.h"
#include "ns3/flow-monitor-module.h"
#include "ns3/log.h"
#include "ns3/point-to-point-helper.h"
#include "ns3/nr-module.h"
#include "ns3/internet-apps-module.h"
#include "ns3/flow-monitor-module.h"
#include "ns3/config-store-module.h"
#include "ns3/spectrum-module.h"
#include <ns3/buildings-helper.h>
#include "ns3/lte-module.h"
#include <iostream>
#include <string>
#include "ns3/trace-source-accessor.h"
#include "ns3/traced-value.h"
#include "ns3/trace-helper.h"









using namespace ns3;

/**
 * \brief Main class
 */
class TestThesis
{

public:

  /**
   * \brief This function converts a linear SINR value that is encapsulated in
   * params structure to dBs, and then it prints the dB value to an output file
   * containing SINR values.
   * @param params RxPacketTraceParams structure that contains different
   * attributes that define the reception of the packet
   *
   */
  void UeReception (RxPacketTraceParams params);

  /**
   * \brief This function converts a linear SNR value to dBs and prints it to
   * the output file containing SNR values.
   * @param snr SNR value in linear units
   */
  void UeSnrPerProcessedChunk (double snr);

  /**
   * \brief This function prints out the RSSI value in dBm to file.
   * @param rssidBm RSSI value in dBm
   */
  void UeRssiPerProcessedChunk (double rssidBm);

  /**
   * Function that will actually configure all the simulation parameters,
   * topology and run the simulation by using the parameters that are being
   * configured for the specific run.
   *
   * @param centralFrequencyBand The band central frequency
   * @param bandwidthBand The band bandwidth
   * @param numerology The numerology
   * @param TxPowerGnb0Bwp0,1,2,3 The gNB0 power,TxPowerGnb1Bwp0,1,2,3 The gNB1 power
   * @param gNbAntennaModel antenna model to be used by gNB device, can be ISO
   * directional 3GPP
   * @param ueAntennaModel antenna model to be used by gNB device, can be ISO
   * directional 3GPP
   * @param testScenario defines the  scenario to be used in the simulation
   * @param speed the speed of UEs in km/h
   * @param resultsDirPath results directory path
   * @param tag A tag that contains some simulation run specific values in order
   * to be able to distinguish the results file for different runs for different
   * parameters configuration
   * @param duration The duration of the simulation
   */
  void Run (double centralFrequencyBand,double bandwidthBand,uint16_t numerology,
            double TxPowerGnb0Bwp0,double TxPowerGnb0Bwp1,double TxPowerGnb0Bwp2,double TxPowerGnb0Bwp3,
            double TxPowerGnb1Bwp0,double TxPowerGnb1Bwp1,double TxPowerGnb1Bwp2,double TxPowerGnb1Bwp3,
            bool cellScan, double beamSearchAngleStep,bool gNbAntennaModel,
            bool ueAntennaModel,bool disableDl,bool disableUl,double speed, std::string outputDir,
            std::string simTag,double lambdaBe,double lambdaUll,std::string testScenario);
  /**
   * \brief Destructor that closes the output file stream and finished the
   * writing into the files.
   */
  ~TestThesis ();



private:

  std::ofstream m_outSinrFile;         //!< the output file stream for the SINR file
  std::ofstream m_outSnrFile;          //!< the output file stream for the SNR file
  std::ofstream m_outRssiFile;         //!< the output file stream for the RSSI file
  std::ofstream m_outUePositionsFile;  //!< the output file stream for the UE positions file
  std::ofstream m_outGnbPositionsFile; //!< the output file stream for the gNB positions file


};

/**
 * Function that creates the output file name for the results.
 * @param directoryName Directory name
 * @param filePrefix The prefix for the file name, e.g. sinr, snr,..
 * @param tag A tag that contains some simulation run specific values and see the results from different runs for different parameters  at configuration
 * @return returns The full path file name string
 */
std::string
BuildFileNameString (std::string directoryName, std::string filePrefix, std::string tag)
{
  std::ostringstream oss;
  oss << directoryName << filePrefix << tag;
  return oss.str ();
}

/**
 * Creates a string tag that contains some simulation run specific values in
 * order to be able to distinguish the results files for different runs for
 * different parameters.
 * @param gNbAntennaModel gNb antenna model
 * @param ueAntennaModel UE antenna model
 * @param scenario The indoor scenario to be used
 * @param speed The speed of UEs in km/h
 * @return the parameter specific simulation name
 */
std::string
BuildTag(bool gNbAntennaModel, bool ueAntennaModel, std::string scenario,
         double speed)
{
  std::ostringstream oss;
  std::string ao;

  std::string gnbAm;
  if (gNbAntennaModel)
    {
      gnbAm = "ISO";
    }
  else
    {
      gnbAm = "3GPP";
    }

  std::string ueAm;
  if (ueAntennaModel)
    {
      ueAm = "ISO";
    }
  else
    {
      ueAm = "3GPP";
    }

  std::string gm = "";
  oss << "-ao" << ao << "-amGnb" << gnbAm << "-amUE" << ueAm <<
      "-sc" << scenario << "-sp" << speed << "-gm" << gm;

  return oss.str ();
}

/**
 * A callback function that redirects a call to the scenario instance.
 * @param scenario A pointer to a simulation instance
 * @param params RxPacketTraceParams structure containing RX parameters
 */
void UeReceptionTrace (TestThesis* scenario, RxPacketTraceParams params)
{
  scenario->UeReception (params);
 }

/**
 * A callback function that redirects a call to the scenario instance.
 * @param scenario A pointer to a simulation instance
 * @param snr SNR value
 */
void UeSnrPerProcessedChunkTrace (TestThesis* scenario, double snr)
{
  scenario->UeSnrPerProcessedChunk (snr);
}

/**
 * A callback function that redirects a call to the scenario instance.
 * @param scenario A pointer to a simulation instance
 * @param rssidBm rssidBm RSSI value in dBm
 */
void UeRssiPerProcessedChunkTrace (TestThesis* scenario, double rssidBm)
{
  scenario->UeRssiPerProcessedChunk (rssidBm);
}


void
TestThesis::UeReception (RxPacketTraceParams params)
{
  m_outSinrFile<<"CELLID:"<<params.m_cellId<<"\t"<<"RNTI:"<<params.m_rnti<<"\t"<<"tbSize:"<<params.m_tbSize<<"\t"<<"FrameNum:"<<params.m_frameNum<<"\t"<<"SlotNumber:"
  <<params.m_slotNum<<"\t"<<"tBler:"<<params.m_tbler<<"\t"<<"BWPID:"<<params.m_bwpId<<"\t"<<"corrupt:"<<params.m_corrupt<<"\t"<< 10*log10 (params.m_sinr) << std::endl;
}

void
TestThesis::UeSnrPerProcessedChunk (double snr)
{
  m_outSnrFile << 10 * log10 (snr) << std::endl;
}


void
TestThesis::UeRssiPerProcessedChunk (double rssidBm)
{
  m_outRssiFile << rssidBm << std::endl;
}

TestThesis::~TestThesis ()
{
  m_outSinrFile.close ();
  m_outSnrFile.close ();
  m_outRssiFile.close ();
}

void
TestThesis::Run (double centralFrequencyBand,double bandwidthBand,uint16_t numerology,
                              double TxPowerGnb0Bwp0,double TxPowerGnb0Bwp1,double TxPowerGnb0Bwp2,double TxPowerGnb0Bwp3,
                              double TxPowerGnb1Bwp0,double TxPowerGnb1Bwp1,double TxPowerGnb1Bwp2,double TxPowerGnb1Bwp3,
                              bool cellScan, double beamSearchAngleStep,bool gNbAntennaModel,
                              bool ueAntennaModel, bool disableDl, bool disableUl, double speed, std::string outputDir,
                              std::string simTag, double lambdaBe, double lambdaUll, std::string testScenario)
  {




      // setup the nr simulation
      Ptr<NrPointToPointEpcHelper> epcHelper = CreateObject<NrPointToPointEpcHelper> ();
      Ptr<IdealBeamformingHelper> idealBeamformingHelper = CreateObject<IdealBeamformingHelper>();
      Ptr<NrHelper> nrHelper = CreateObject<NrHelper> ();

      nrHelper->SetIdealBeamformingHelper(idealBeamformingHelper);
      nrHelper->SetEpcHelper (epcHelper);


      // creation of simulation tag in case is not provided
      if (simTag=="")
        {
          simTag = BuildTag (gNbAntennaModel, ueAntennaModel, testScenario, speed);
        }
      std::string filenameSinr = BuildFileNameString ( outputDir , "sinrs", simTag);
      std::string filenameSnr = BuildFileNameString ( outputDir , "snrs", simTag);
      std::string filenameRssi = BuildFileNameString ( outputDir , "rssi", simTag);
      std::string filenameUePositions = BuildFileNameString ( outputDir , "ue-positions", simTag);
      std::string filenameGnbPositions = BuildFileNameString( outputDir , "gnb-positions", simTag);

      m_outSinrFile.open (filenameSinr.c_str ());
      m_outSinrFile.setf (std::ios_base::fixed);

      if(!m_outSinrFile.is_open ())
        {
          NS_ABORT_MSG("Can't open file " << filenameSinr);
        }

      m_outSnrFile.open (filenameSnr.c_str ());
      m_outSnrFile.setf (std::ios_base::fixed);

      if(!m_outSnrFile.is_open ())
        {
          NS_ABORT_MSG("Can't open file " << filenameSnr);
        }

      m_outRssiFile.open (filenameRssi.c_str ());
      m_outRssiFile.setf (std::ios_base::fixed);

      if(!m_outRssiFile.is_open())
        {
          NS_ABORT_MSG("Can't open file " << filenameRssi);
        }

      m_outUePositionsFile.open (filenameUePositions.c_str ());
      m_outUePositionsFile.setf (std::ios_base::fixed);

      if(!m_outUePositionsFile.is_open ())
        {
          NS_ABORT_MSG("Can't open file " << filenameUePositions);
        }

      m_outGnbPositionsFile.open (filenameGnbPositions.c_str ());
      m_outGnbPositionsFile.setf (std::ios_base::fixed);

      if(!m_outGnbPositionsFile.is_open ())
        {
          NS_ABORT_MSG("Can't open file " << filenameGnbPositions);
        }


        // create base stations and mobile terminals
          NodeContainer gNbNodes;
          NodeContainer ueNodes;
          MobilityHelper mobility;

          uint32_t gNbNum = 2;
          uint32_t ueNumPergNb = 2;
          uint16_t numFlowsUe = 4;
          double simTime = 0.9; // seconds
          double udpAppStartTime = 0.5; //seconds
          uint32_t udpPacketSizeBe = 905;

          // BS antenna height is 3 meters
          double gNbHeight = 3;
          // UE antenna height is 1.5 meters
          double ueHeight = 1.5;

          gNbNodes.Create (gNbNum);
          ueNodes.Create (ueNumPergNb * gNbNum);

          // Positions of the gNBs
          Ptr<ListPositionAllocator> gNbPositionAlloc = CreateObject<ListPositionAllocator> ();

          for (uint8_t j = 0; j < 2; j++)
            {
              for (uint8_t i = 0; i < 6; i++)
                {
                  gNbPositionAlloc->Add (Vector ( i*20, j*20, gNbHeight));
                }
            }

          mobility.SetMobilityModel ("ns3::ConstantPositionMobilityModel");
          mobility.SetPositionAllocator (gNbPositionAlloc);
          mobility.Install (gNbNodes);

          double minBigBoxX = -10.0;
          double minBigBoxY = -15.0;
          double maxBigBoxX = 110.0;
          double maxBigBoxY =  35.0;

          // Positions of the UEs

          for (uint8_t j = 0; j < 2; j++)
            {
              double minSmallBoxY = minBigBoxY + j * (maxBigBoxY - minBigBoxY) / 2;

              for (uint8_t i = 0; i < 6; i++)
                {
                  double minSmallBoxX = minBigBoxX + i * (maxBigBoxX - minBigBoxX) / 6;
                  Ptr<UniformRandomVariable> ueRandomVarX = CreateObject<UniformRandomVariable> ();

                  double minX = minSmallBoxX;
                  double maxX = minSmallBoxX + (maxBigBoxX - minBigBoxX) / 6 - 0.0001;
                  double minY = minSmallBoxY;
                  double maxY = minSmallBoxY + (maxBigBoxY-minBigBoxY) / 2 - 0.0001;

                  Ptr<RandomBoxPositionAllocator> ueRandomRectPosAlloc = CreateObject<RandomBoxPositionAllocator> ();
                  ueRandomVarX->SetAttribute ("Min", DoubleValue (minX));
                  ueRandomVarX->SetAttribute ("Max", DoubleValue (maxX));
                  ueRandomRectPosAlloc->SetX (ueRandomVarX);
                  Ptr<UniformRandomVariable> ueRandomVarY = CreateObject<UniformRandomVariable> ();
                  ueRandomVarY->SetAttribute ("Min", DoubleValue (minY));
                  ueRandomVarY->SetAttribute ("Max", DoubleValue (maxY));
                  ueRandomRectPosAlloc->SetY (ueRandomVarY);
                  Ptr<ConstantRandomVariable> ueRandomVarZ = CreateObject<ConstantRandomVariable> ();
                  ueRandomVarZ->SetAttribute ("Constant", DoubleValue (ueHeight));
                  ueRandomRectPosAlloc->SetZ (ueRandomVarZ);


                  mobility.SetPositionAllocator (ueRandomRectPosAlloc);
                  mobility.Install (ueNodes);

                }
            }

            for (uint32_t j = 0; j < ueNodes.GetN (); j++)
              {
                  Vector v = ueNodes.Get (j)->GetObject<MobilityModel> ()->GetPosition ();
                  m_outUePositionsFile << j << "\t" << v.x << "\t" << v.y << "\t" << v.z << " " << std::endl;
              }

            for (uint32_t j = 0; j < gNbNodes.GetN (); j++)
              {
                  Vector v = gNbNodes.Get (j)->GetObject<MobilityModel> ()->GetPosition ();
                  m_outGnbPositionsFile << j << "\t" << v.x << "\t" << v.y << "\t" << v.z << " " << std::endl;
              }

            m_outUePositionsFile.close ();
            m_outGnbPositionsFile.close ();

            BandwidthPartInfo::Scenario scenario;
            if (testScenario=="UMa")
              {

                scenario = BandwidthPartInfo::UMa;
              }
              else
              {
                NS_ABORT_MSG ("Unsupported scenario");
              }


      /*
       * Setup the configuration of the spectrum
       */

      BandwidthPartInfoPtrVector allBwps;
      CcBwpCreator ccBwpCreator;

      OperationBandInfo band;





          /*

           *
           * The configured spectrum division is:
           * ----------------------------- Band --------------------------------
           * ------CC0------|------CC1-------|-------CC2-------|-------CC3-------
           * ------BWP0-----|------BWP0------|-------BWP0------|-------BWP0------
           */

          const uint8_t numContiguousCcs = 4; // 4 CCs per Band

          // Configuration of the band
          CcBwpCreator::SimpleOperationBandConf bandConf (centralFrequencyBand, bandwidthBand,
                                                          numContiguousCcs,scenario);

          bandConf.m_numBwp = 1; // 1 BWP per CC

          //creation of the band
          band = ccBwpCreator.CreateOperationBandContiguousCc (bandConf);




      nrHelper->SetPathlossAttribute ("ShadowingEnabled", BooleanValue (false));
      epcHelper->SetAttribute ("S1uLinkDelay", TimeValue (MilliSeconds (0)));
      nrHelper->SetSchedulerAttribute ("UlCtrlSymbols", UintegerValue (1));
      nrHelper->SetSchedulerTypeId (TypeId::LookupByName ("ns3::NrMacSchedulerTdmaRR"));
      // Beamforming method
      if (cellScan)
      {
        idealBeamformingHelper->SetAttribute ("IdealBeamformingMethod", TypeIdValue (CellScanBeamforming::GetTypeId ()));
        idealBeamformingHelper->SetIdealBeamFormingAlgorithmAttribute ("BeamSearchAngleStep", DoubleValue (beamSearchAngleStep));
      }
      else
      {
        idealBeamformingHelper->SetAttribute ("IdealBeamformingMethod", TypeIdValue (DirectPathBeamforming::GetTypeId ()));
      }

      nrHelper->InitializeOperationBand (&band);
      allBwps = CcBwpCreator::GetAllBwps ({band});



      // Antennas for all the UEs
      nrHelper->SetUeAntennaAttribute ("NumRows", UintegerValue (2));
      nrHelper->SetUeAntennaAttribute ("NumColumns", UintegerValue (4));
      nrHelper->SetUeAntennaAttribute ("IsotropicElements", BooleanValue (ueAntennaModel));

      // Antennas for all the gNbs
      nrHelper->SetGnbAntennaAttribute ("NumRows", UintegerValue (4));
      nrHelper->SetGnbAntennaAttribute ("NumColumns", UintegerValue (8));
      nrHelper->SetGnbAntennaAttribute ("IsotropicElements", BooleanValue (gNbAntennaModel));


      uint32_t bwpIdForLowLat = 0;
      uint32_t bwpIdForVoice = 1;
      uint32_t bwpIdForVideo = 2;
      uint32_t bwpIdForVideoGaming = 3;

      nrHelper->SetGnbBwpManagerAlgorithmAttribute ("NGBR_LOW_LAT_EMBB", UintegerValue (bwpIdForLowLat));
      nrHelper->SetGnbBwpManagerAlgorithmAttribute ("GBR_CONV_VOICE", UintegerValue (bwpIdForVoice));
      nrHelper->SetGnbBwpManagerAlgorithmAttribute ("NGBR_VIDEO_TCP_PREMIUM", UintegerValue (bwpIdForVideo));
      nrHelper->SetGnbBwpManagerAlgorithmAttribute ("NGBR_VOICE_VIDEO_GAMING", UintegerValue (bwpIdForVideoGaming));

      //Install and get the pointers to the NetDevices
      NetDeviceContainer gnbNetDev = nrHelper->InstallGnbDevice (gNbNodes, allBwps);
      NetDeviceContainer ueNetDev = nrHelper->InstallUeDevice (ueNodes, allBwps);



          // Set the attribute of the netdevice (gnbNetDev.Get (0)) and bandwidth part (0), (1), ...
          nrHelper->GetGnbPhy (gnbNetDev.Get (0), 0)->SetAttribute ("Numerology", UintegerValue (numerology));
          nrHelper->GetGnbPhy (gnbNetDev.Get (0), 0)->SetAttribute ("TxPower", DoubleValue (10*log10(TxPowerGnb0Bwp0)));


          nrHelper->GetGnbPhy (gnbNetDev.Get (0), 1)->SetAttribute ("Numerology", UintegerValue (numerology));
          nrHelper->GetGnbPhy (gnbNetDev.Get (0), 1)->SetAttribute ("TxPower", DoubleValue (10*log10(TxPowerGnb0Bwp1)));

          nrHelper->GetGnbPhy (gnbNetDev.Get (0), 2)->SetAttribute ("Numerology", UintegerValue (numerology));
          nrHelper->GetGnbPhy (gnbNetDev.Get (0), 2)->SetAttribute ("TxPower", DoubleValue (10*log10(TxPowerGnb0Bwp2)));

          nrHelper->GetGnbPhy (gnbNetDev.Get (0), 3)->SetAttribute ("Numerology", UintegerValue (numerology));
          nrHelper->GetGnbPhy (gnbNetDev.Get (0), 3)->SetAttribute ("TxPower", DoubleValue (10*log10(TxPowerGnb0Bwp3)));

          // Set the attribute of the netdevice (gnbNetDev.Get (1)) and bandwidth part (0), (1), ...
          nrHelper->GetGnbPhy (gnbNetDev.Get (1), 0)->SetAttribute ("Numerology", UintegerValue (numerology));
          nrHelper->GetGnbPhy (gnbNetDev.Get (1), 0)->SetAttribute ("TxPower", DoubleValue (10*log10(TxPowerGnb1Bwp0)));

          nrHelper->GetGnbPhy (gnbNetDev.Get (1), 1)->SetAttribute ("Numerology", UintegerValue (numerology));
          nrHelper->GetGnbPhy (gnbNetDev.Get (1), 1)->SetAttribute ("TxPower", DoubleValue (10*log10(TxPowerGnb1Bwp1)));

          nrHelper->GetGnbPhy (gnbNetDev.Get (1), 2)->SetAttribute ("Numerology", UintegerValue (numerology));
          nrHelper->GetGnbPhy (gnbNetDev.Get (1), 2)->SetAttribute ("TxPower", DoubleValue (10*log10(TxPowerGnb1Bwp2)));

          nrHelper->GetGnbPhy (gnbNetDev.Get (1), 3)->SetAttribute ("Numerology", UintegerValue (numerology));
          nrHelper->GetGnbPhy (gnbNetDev.Get (1), 3)->SetAttribute ("TxPower", DoubleValue (10*log10(TxPowerGnb1Bwp3)));





      for (auto it = gnbNetDev.Begin (); it != gnbNetDev.End (); ++it)
        {
          DynamicCast<NrGnbNetDevice> (*it)->UpdateConfig ();
        }

      for (auto it = ueNetDev.Begin (); it != ueNetDev.End (); ++it)
        {
          DynamicCast<NrUeNetDevice> (*it)->UpdateConfig ();
        }


      // create the internet and install the IP stack on the UEs
      // get SGW/PGW and create a single RemoteHost
      Ptr<Node> pgw = epcHelper->GetPgwNode ();
      NodeContainer remoteHostContainer;
      remoteHostContainer.Create (1);
      Ptr<Node> remoteHost = remoteHostContainer.Get (0);
      InternetStackHelper internet;
      internet.Install (remoteHostContainer);

      // connect a remoteHost to pgw and setup routing
      PointToPointHelper p2ph;
      p2ph.SetDeviceAttribute ("DataRate", DataRateValue (DataRate ("100Gb/s")));
      p2ph.SetDeviceAttribute ("Mtu", UintegerValue (2500));
      p2ph.SetChannelAttribute ("Delay", TimeValue (Seconds (0.010)));
      NetDeviceContainer internetDevices = p2ph.Install (pgw, remoteHost);
      Ipv4AddressHelper ipv4h;
      Ipv4StaticRoutingHelper ipv4RoutingHelper;
      ipv4h.SetBase ("1.0.0.0", "255.0.0.0");
      Ipv4InterfaceContainer internetIpIfaces = ipv4h.Assign (internetDevices);
      Ptr<Ipv4StaticRouting> remoteHostStaticRouting = ipv4RoutingHelper.GetStaticRouting (remoteHost->GetObject<Ipv4> ());
      remoteHostStaticRouting->AddNetworkRouteTo (Ipv4Address ("7.0.0.0"), Ipv4Mask ("255.0.0.0"), 1);
      internet.Install (ueNodes);
      Ipv4InterfaceContainer ueIpIface;
      ueIpIface = epcHelper->AssignUeIpv4Address (NetDeviceContainer (ueNetDev));

      Ipv4Address remoteHostAddr = internetIpIfaces.GetAddress (1);

      // Set the default gateway for the UEs
      for (uint32_t j = 0; j < ueNodes.GetN (); ++j)
        {
          Ptr<Ipv4StaticRouting> ueStaticRouting =
                  ipv4RoutingHelper.GetStaticRouting (ueNodes.Get (j)->GetObject<Ipv4> ());
          ueStaticRouting->SetDefaultRoute (epcHelper->GetUeDefaultGatewayAddress (), 1);
        }

      // attach UEs to the closest eNB before creating the dedicated flows
      nrHelper->AttachToClosestEnb (ueNetDev, gnbNetDev);

      // install UDP applications
      uint16_t dlPort = 1234;
      uint16_t ulPort = dlPort + gNbNum * ueNumPergNb * numFlowsUe + 1;
      ApplicationContainer clientApps, serverApps;

      for (uint32_t u = 0; u < ueNodes.GetN(); ++u)
        {
          for (uint16_t flow = 0; flow < numFlowsUe; ++flow)
            {
              if (!disableDl)
                {
                  PacketSinkHelper dlPacketSinkHelper ("ns3::UdpSocketFactory", InetSocketAddress (Ipv4Address::GetAny (), dlPort));
                  serverApps.Add (dlPacketSinkHelper.Install (ueNodes.Get (u)));

                  UdpClientHelper dlClient (ueIpIface.GetAddress (u), dlPort);
                  dlClient.SetAttribute("PacketSize", UintegerValue(udpPacketSizeBe));
                  dlClient.SetAttribute ("Interval", TimeValue (Seconds(1.0/lambdaUll)));
                  dlClient.SetAttribute ("MaxPackets", UintegerValue(0xFFFFFFFF));
                  clientApps.Add (dlClient.Install (remoteHost));

                  Ptr<EpcTft> tft = Create<EpcTft> ();
                  EpcTft::PacketFilter dlpf;
                  dlpf.localPortStart = dlPort;
                  dlpf.localPortEnd = dlPort;
                  ++dlPort;
                  tft->Add (dlpf);

                  enum EpsBearer::Qci q;
                  if (flow == 0)
                    {
                      q = EpsBearer::NGBR_LOW_LAT_EMBB;
                    }
                  else if (flow == 1)
                    {
                      q = EpsBearer::GBR_CONV_VOICE;
                    }
                  else if (flow == 2)
                    {
                      q = EpsBearer::NGBR_VIDEO_TCP_PREMIUM;
                    }
                  else if (flow == 3)
                    {
                      q = EpsBearer::NGBR_VOICE_VIDEO_GAMING;
                    }
                  else
                    {
                      q = EpsBearer::NGBR_VIDEO_TCP_DEFAULT;
                    }
                  EpsBearer bearer (q);
                  nrHelper->ActivateDedicatedEpsBearer(ueNetDev.Get(u), bearer, tft);
                }

              if (!disableUl)
                {
                  PacketSinkHelper ulPacketSinkHelper ("ns3::UdpSocketFactory", InetSocketAddress (Ipv4Address::GetAny (), ulPort));
                  serverApps.Add (ulPacketSinkHelper.Install (remoteHost));

                  UdpClientHelper ulClient (remoteHostAddr, ulPort);
                  ulClient.SetAttribute("PacketSize", UintegerValue(udpPacketSizeBe));
                  ulClient.SetAttribute ("Interval", TimeValue (Seconds(1.0/lambdaUll)));
                  ulClient.SetAttribute ("MaxPackets", UintegerValue(0xFFFFFFFF));
                  clientApps.Add (ulClient.Install (ueNodes.Get(u)));

                  Ptr<EpcTft> tft = Create<EpcTft> ();
                  EpcTft::PacketFilter ulpf;
                  ulpf.remotePortStart = ulPort;
                  ulpf.remotePortEnd = ulPort;
                  ++ulPort;
                  tft->Add (ulpf);

                  enum EpsBearer::Qci q;
                  if (flow == 0)
                    {
                      q = EpsBearer::NGBR_LOW_LAT_EMBB;
                    }
                  else if (flow == 1)
                    {
                      q = EpsBearer::GBR_CONV_VOICE;
                    }
                  else if (flow == 2)
                    {
                      q = EpsBearer::NGBR_VIDEO_TCP_PREMIUM;
                    }
                  else if (flow == 3)
                    {
                      q = EpsBearer::NGBR_VOICE_VIDEO_GAMING;
                    }
                  else
                    {
                      q = EpsBearer::NGBR_VIDEO_TCP_DEFAULT;
                    }
                  EpsBearer bearer (q);
                  nrHelper->ActivateDedicatedEpsBearer(ueNetDev.Get(u), bearer, tft);
                }

            }
        }

      // start UDP server and client apps
      serverApps.Start (Seconds (udpAppStartTime));
      clientApps.Start (Seconds (udpAppStartTime));
      serverApps.Stop (Seconds (simTime));
      clientApps.Stop (Seconds (simTime));


      // enable the traces
      nrHelper->EnableTraces();

      for (uint32_t q = 0 ; q < ueNetDev.GetN (); q ++)
        {
          Ptr<NrSpectrumPhy > ue1SpectrumPhy = DynamicCast<NrUeNetDevice>
          (ueNetDev.Get (q))->GetPhy (q)->GetSpectrumPhy ();
          ue1SpectrumPhy->TraceConnectWithoutContext ("RxPacketTraceUe", MakeBoundCallback (&UeReceptionTrace, this));
          Ptr<nrInterference> ue1SpectrumPhyInterference = ue1SpectrumPhy->GetNrInterference ();
          NS_ABORT_IF (!ue1SpectrumPhyInterference);
          NS_LOG_UNCOND ("RxPacketTraceUe start for UE: " << q << std::endl);
          ue1SpectrumPhyInterference->TraceConnectWithoutContext ("SnrPerProcessedChunk", MakeBoundCallback (&UeSnrPerProcessedChunkTrace, this));
          ue1SpectrumPhyInterference->TraceConnectWithoutContext ("RssiPerProcessedChunk", MakeBoundCallback (&UeRssiPerProcessedChunkTrace, this));
        }

      FlowMonitorHelper flowmonHelper;
      NodeContainer endpointNodes;
      endpointNodes.Add (remoteHost);
      endpointNodes.Add (ueNodes);

      Ptr<ns3::FlowMonitor> monitor = flowmonHelper.Install (endpointNodes);
      monitor->SetAttribute ("DelayBinWidth", DoubleValue (0.001));
      monitor->SetAttribute ("JitterBinWidth", DoubleValue (0.001));
      monitor->SetAttribute ("PacketSizeBinWidth", DoubleValue (20));




        Simulator::Stop (Seconds (simTime));
        Simulator::Run ();




      // Print per-flow statistics
      monitor->CheckForLostPackets ();
      Ptr<Ipv4FlowClassifier> classifier = DynamicCast<Ipv4FlowClassifier> (flowmonHelper.GetClassifier ());
      FlowMonitor::FlowStatsContainer stats = monitor->GetFlowStats ();

      double averageFlowThroughput = 0.0;
      double averageFlowDelay = 0.0;

      std::ofstream outFile;
      std::string filename = outputDir + "/" + simTag;
      outFile.open (filename.c_str (), std::ofstream::out | std::ofstream::trunc);
      if (!outFile.is_open ())
        {
          NS_ABORT_MSG("Can't open file "  << filename << std::endl);

        }

      outFile.setf (std::ios_base::fixed);

      for (std::map<FlowId, FlowMonitor::FlowStats>::const_iterator i = stats.begin (); i != stats.end (); ++i)
        {
          Ipv4FlowClassifier::FiveTuple t = classifier->FindFlow (i->first);
          std::stringstream protoStream;
          protoStream << (uint16_t) t.protocol;
          if (t.protocol == 6)
            {
              protoStream.str ("TCP");
            }
          if (t.protocol == 17)
            {
              protoStream.str ("UDP");
            }
          outFile << "Flow " << i->first << " (" << t.sourceAddress << ":" << t.sourcePort << " -> " << t.destinationAddress << ":" << t.destinationPort << ") proto " << protoStream.str () << "\n";
          outFile << "  Tx Packets: " << i->second.txPackets << "\n";
          outFile << "  Tx Bytes:   " << i->second.txBytes << "\n";
          outFile << "  TxOffered:  " << i->second.txBytes * 8.0 / (simTime - udpAppStartTime) / 1000 / 1000  << " Mbps\n";
          outFile << "  Rx Bytes:   " << i->second.rxBytes << "\n";
          if (i->second.rxPackets > 0)
            {
              // Measure the duration of the flow from receiver's perspective
              double rxDuration = (simTime - udpAppStartTime);

              averageFlowThroughput += i->second.rxBytes * 8.0 / rxDuration / 1000 / 1000;
              averageFlowDelay += 1000 * i->second.delaySum.GetSeconds () / i->second.rxPackets;

              outFile << "  Throughput: " << i->second.rxBytes * 8.0 / rxDuration / 1000 / 1000  << " Mbps\n";
              outFile << "  Mean delay:  " << 1000 * i->second.delaySum.GetSeconds () / i->second.rxPackets << " ms\n";
              outFile << "  Mean jitter:  " << 1000 * i->second.jitterSum.GetSeconds () / i->second.rxPackets  << " ms\n";
            }
          else
            {
              outFile << "  Throughput:  0 Mbps\n";
              outFile << "  Mean delay:  0 ms\n";
              outFile << "  Mean jitter: 0 ms\n";
            }
          outFile << "  Rx Packets: " << i->second.rxPackets << "\n";
        }

      outFile << "\n\n  Mean flow throughput: " << averageFlowThroughput / stats.size () << "\n";
      outFile << "  Mean flow delay: " << averageFlowDelay / stats.size () << "\n";

      outFile.close ();

      std::ifstream f (filename.c_str ());

      if (f.is_open ())
        {
          std::cout << f.rdbuf ();
        }

      Simulator::Destroy ();
}
int
main (int argc, char *argv[])
{


  uint8_t numBands = 1;
  double centralFrequencyBand = 20e9;
  double bandwidthBand = 1e9;
  uint16_t numerology = 3;
  bool gNbAntennaModel = true;
  bool ueAntennaModel = true;
  std::string testScenario = "UMa";


  double TxPowerGnb0Bwp0 = 10.0;
  double TxPowerGnb0Bwp1 = 10.0;
  double TxPowerGnb0Bwp2 = 10.0;
  double TxPowerGnb0Bwp3 = 10.0;

  double TxPowerGnb1Bwp0 = 10.0;
  double TxPowerGnb1Bwp1 = 10.0;
  double TxPowerGnb1Bwp2 = 10.0;
  double TxPowerGnb1Bwp3 = 10.0;

  bool cellScan = false;
  double beamSearchAngleStep = 10.0;
  uint32_t lambdaUll = 1000;
  uint32_t lambdaBe = 100;
  bool logging = false;
  bool disableDl = false;
  bool disableUl = true;
  double speed = 3.00;

  std::string simTag = "default";
  std::string outputDir = "./";


  CommandLine cmd;

  cmd.AddValue ("TxPowerGnb0Bwp0",
                "TxPower to be used for gnb0, BWP 1",
                TxPowerGnb0Bwp0);
  cmd.AddValue ("TxPowerGnb0Bwp1",
                "TxPower to be used for gnb0, BWP 2",
                TxPowerGnb0Bwp1);
  cmd.AddValue ("TxPowerGnb0Bwp2",
                "TxPower to be used for gnb0, BWP 3",
                TxPowerGnb0Bwp2);
  cmd.AddValue ("TxPowerGnb0Bwp3",
                "TxPower to be used for gnb0, BWP 4",
                TxPowerGnb0Bwp3);
  cmd.AddValue ("TxPowerGnb1Bwp0",
                "TxPower to be used for gnb1, BWP 1",
                TxPowerGnb1Bwp0);
  cmd.AddValue ("TxPowerGnb1Bwp1",
                "TxPower to be used for gnb1, BWP 2",
                TxPowerGnb1Bwp1);
  cmd.AddValue ("TxPowerGnb1Bwp2",
                "TxPower to be used for gnb1, BWP 3",
                TxPowerGnb1Bwp2);
  cmd.AddValue ("TxPowerGnb1Bwp3",
                "TxPower to be used for gnb1, BWP 4",
                TxPowerGnb1Bwp3);
  cmd.AddValue ("testScenario",
                "The test scenario ",
                testScenario);
  cmd.AddValue ("speed",
                "UE speed in km/h",
                speed);
  cmd.AddValue ("gNbAntennaModel",
                "Enable Isotropic antenna for the gNB",
                gNbAntennaModel);
  cmd.AddValue ("ueAntennaModel",
                "Enable Isotropic antenna for the UE",
                ueAntennaModel);
  cmd.AddValue ("numBands",
                "Number of operation bands",
                numBands);
  cmd.AddValue ("centralFrequencyBand",
                "The system frequency to be used in band ",
                centralFrequencyBand);
  cmd.AddValue ("bandwidthBand",
                "The system bandwidth to be used in band",
                bandwidthBand);
  cmd.AddValue ("numerology",
                "Numerology",
                numerology);
  cmd.AddValue ("cellScan",
                "Use beam search method to determine beamforming vector,"
                "true to use cell scanning method",
                cellScan);
  cmd.AddValue ("beamSearchAngleStep",
                "Beam search angle step for beam search method",
                beamSearchAngleStep);
  cmd.AddValue ("lambdaUll",
                "Number of UDP packets in one second for ultra low latency traffic",
                lambdaUll);
  cmd.AddValue ("lambdaBe",
                "Number of UDP packets in one second for best effort traffic",
                lambdaBe);
  cmd.AddValue ("logging",
                "Enable logging",
                logging);
  cmd.AddValue ("disableDl",
                "Disable DL flow",
                disableDl);
  cmd.AddValue ("disableUl",
                "Disable UL flow",
                disableUl);
  cmd.AddValue ("simTag",
                "tag to be appended to output filenames",
                simTag);
  cmd.AddValue ("outputDir",
                "directory where to store simulation results",
                outputDir);

  cmd.Parse (argc, argv);

  NS_ABORT_IF (numBands < 1);
  NS_ABORT_MSG_IF (disableDl==true && disableUl==true, "Enable one of the flows");

  //ConfigStore inputConfig;
  //inputConfig.ConfigureDefaults ();

  // enable logging or not
  if (logging)
    {
    //  LogComponentEnable ("Nr3gppPropagationLossModel", LOG_LEVEL_ALL);
        //LogComponentEnable ("Nr3gppChannel", LOG_LEVEL_ALL);
    //  LogComponentEnable ("UdpClient", LOG_LEVEL_INFO);
    //  LogComponentEnable ("UdpServer", LOG_LEVEL_INFO);
    //  LogComponentEnable ("LtePdcp", LOG_LEVEL_INFO);
      LogComponentEnable ("NrGnbPhy", LOG_LEVEL_INFO);
      LogComponentEnable ("NrUePhy", LOG_LEVEL_INFO);
    }

  Config::SetDefault ("ns3::LteRlcUm::MaxTxBufferSize", UintegerValue (999999999));

  TestThesis TestScenario;
  TestScenario.Run(centralFrequencyBand,bandwidthBand, numerology,TxPowerGnb0Bwp0,TxPowerGnb0Bwp1,TxPowerGnb0Bwp2,TxPowerGnb0Bwp3,
                                TxPowerGnb1Bwp0, TxPowerGnb1Bwp1, TxPowerGnb1Bwp2, TxPowerGnb1Bwp3, cellScan, beamSearchAngleStep, gNbAntennaModel,
                                ueAntennaModel, disableDl,  disableUl, speed,  outputDir, simTag,
                                lambdaBe, lambdaUll,testScenario);
  return 0;
}

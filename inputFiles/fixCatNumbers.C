void fixCatNumbers(TString inFileName) {
  
  TFile *oldFile= new TFile(inFileName);
  TTree *oldTree = (TTree*)oldFile->Get("m_llg_DATA");

  double oldCat0, oldCat1, oldCat2, oldCat3, oldCat4, oldCat5;
  oldTree->SetBranchAddress("m_llg_DATA",&oldCat0);
  oldTree->SetBranchAddress("m_llgCAT1_DATA",&oldCat1);
  oldTree->SetBranchAddress("m_llgCAT2_DATA",&oldCat2);
  oldTree->SetBranchAddress("m_llgCAT3_DATA",&oldCat3);
  oldTree->SetBranchAddress("m_llgCAT4_DATA",&oldCat4);
  oldTree->SetBranchAddress("m_llgCAT5_DATA",&oldCat5);

  double newCat0, newCat1, newCat2, newCat3, newCat4, newCat5;
  TFile *newFile = new TFile("catFix_"+inFileName,"recreate");
  TTree *newTree = new TTree("m_llg_DATA","m_llg_DATA");
  newTree->Branch("m_llg_DATA",&newCat0);
  newTree->Branch("m_llgCAT1_DATA",&newCat1);
  newTree->Branch("m_llgCAT2_DATA",&newCat2);
  newTree->Branch("m_llgCAT3_DATA",&newCat3);
  newTree->Branch("m_llgCAT4_DATA",&newCat4);
  newTree->Branch("m_llgCAT5_DATA",&newCat5);

  for( int i=0; i<oldTree->GetEntries(); i++ ) {
    newCat0 = newCat1 = newCat2 = newCat3 = newCat4 = newCat5;
    oldTree->GetEntry(i);
    newCat0= oldCat0;
    newCat1= oldCat1;
    newCat2= oldCat4;
    newCat3= oldCat2;
    newCat4= oldCat3;
    newCat5= oldCat5;
    newTree->Fill();
  }

  newFile->Write();
}



##### Convert a txt file to a fasta file and remove the priming regions
##### Tomoya Imai 2025/6/29; seqkit is required
### Input the parameters used in this script
file_in="L34339_Read_Count.txt" #入力ファイル名
pr_F="TCATCCGGAAATTTTGGTTC" #Forward primer sequence
pr_R="AGGAACAGGGAGAACCTCG" #Reverse primer sequence

### Make a directory to keep the files used in the trimming process 
mkdir ./tochu 

### txt to fasta, KYOw ID ($5) is added to the sequence name 
awk -F'\t' 'NR > 1 {print ">"$1"_"$5"\n"$2}' "$file_in"> ./tochu/All.fasta

### Trim the forward primer
seqkit fx2tab -nl ./tochu/All.fasta > ./tochu/lengths.txt # Calculate the length of the lead
seqkit locate -p "$pr_F" -m 0 ./tochu/All.fasta -j 4 > ./tochu/primerF_positions.txt # Find the forward-primer regions
# A bed file is prepaered from the lnegth and the location information obatained above, which is subsuquently used for trimming
awk 'NR==FNR {len[$1]=$2; next}
     NR>1 {
       if ($4 == "+") { s=$6+1; e=len[$1] }
       else if ($4 == "-") { s=0; e=$5-1 }
       if (s < e) print $1"\t"s"\t"e
     }' ./tochu/lengths.txt ./tochu/primerF_positions.txt > ./tochu/rangesF.bed
seqkit subseq --bed ./tochu/rangesF.bed ./tochu/All.fasta > ./tochu/Trimmed_forward.fasta

### Trim the forward primer
seqkit fx2tab -nl ./tochu/Trimmed_forward.fasta > ./tochu/lengths2.txt # Calculate the length of the lead
seqkit locate -p "$pr_R" -m 0 ./tochu/Trimmed_forward.fasta -j 4 > ./tochu/primerR_positions.txt # Find the reverse-primer regions
# A bed file is prepaered from the lnegth and the location information obatained above, which is subsuquently used for trimming
awk 'NR==FNR {len[$1]=$2; next}
     NR>1 {
       if ($4 == "+") { s=$6+1; e=len[$1] }
       else if ($4 == "-") { s=0; e=$5-1 }
       if (s < e) print $1"\t"s"\t"e
     }' ./tochu/lengths2.txt ./tochu/primerR_positions.txt > ./tochu/rangesR.bed
seqkit subseq --bed ./tochu/rangesR.bed ./tochu/Trimmed_forward.fasta > Trimmed_All.fasta
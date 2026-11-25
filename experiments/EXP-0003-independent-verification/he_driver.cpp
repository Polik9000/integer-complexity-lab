// EXP-0003 driver (MIT, ours). Compiles He's GPL single.cpp (hqztrue/integer_complexity@742e8c5)
// unmodified; only renames two symbols that clash on Linux. Not vendored.
#define _init _init_hqz
#define main main_orig
#include "single.cpp"
#undef main
int main(int argc,char**argv){
	init(1e8,1e38);
	int k0=atoi(argv[1]),k1=atoi(argv[2]);
	for(int k=k0;k<=k1;++k){
		u128 n=((u128)1<<k)-1;
		clock_t t=clock();
		clear();
		int v=calc_single(n);
		fprintf(stderr,"");
		printf("{\"k\": %d, \"hqz\": %d, \"sec\": %.2f}\n",k,v,(double)(clock()-t)/CLOCKS_PER_SEC);
		fflush(stdout);
	}
	return 0;
}

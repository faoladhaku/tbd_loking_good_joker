#include <bits/stdc++.h>
#include <omp.h>
using namespace std;

typedef float decimal;
unordered_map<string,unordered_map<string,decimal> > map_rating;
//vector<string,unordered_map<string,decimal> > map_rating;
//map<string,map<string,decimal>> matrix_desviations;
unordered_map<string,unordered_map<string,pair<int,decimal>> > matrix_desviations;

//map<string,map<string,decimal> > map_rating;
//map<decimal, string> map_knn; // mantenerlo ordenado, los mayores primero
//map<decimal, string> map_proyeccion;
//map<string,pair<decimal,decimal> > map_recomendacion;

//string path ="../../ml-latest/";
string path ="../";


vector<string> vec_user;
map<string, string> map_name_movies;


void load_info_names(){

	ifstream archivo_entrada(path+"movies.csv");
    string linea;
    char delim = ',';
    getline(archivo_entrada, linea);
    string cons1;
    string cons2;
    string cons3;
    while(getline(archivo_entrada, linea)) {
        stringstream ss(linea);

    	getline(ss,cons1,delim);
    	getline(ss,cons2,delim);
		map_name_movies[cons1] = cons2;

    }
    archivo_entrada.close();
}

void load_data(){

	//ifstream archivo_entrada("Movie_Ratings_ to_load.csv");
	ifstream archivo_entrada(path+"ratings.csv");
    string linea;
    char delim = ',';
    getline(archivo_entrada, linea);
    string cons1;
    string cons2;
    string cons3;
    while(getline(archivo_entrada, linea)) {
        stringstream ss(linea);

    	getline(ss,cons1,delim);
    	getline(ss,cons2,delim);
    	getline(ss,cons3,delim);
    	if(map_rating.find(cons1) == map_rating.end() ) vec_user.push_back(cons1);
		map_rating[cons2][cons1] = atof(cons3.c_str() );

    }
    archivo_entrada.close();
}

pair<int,decimal> get_variance (string item1,string item2)
{
	if(item1==item2)return make_pair(0,0);
	decimal numerator=0;
	decimal card=0;
	for (auto temp_1:map_rating[item1])
	{
		unordered_map<string,decimal>::iterator found= map_rating[item2].find(temp_1.first);
		if(found!=map_rating[item2].end()){
			numerator+=temp_1.second-found->second;
			card++;
		}
	}
	if(card==0)return make_pair(0,0);
	return  make_pair(card,numerator/card);	
}
void set_iter(unordered_map<string,unordered_map<string,decimal>>::iterator &it,
				int step,
				unordered_map<string,unordered_map<string,decimal>> &u_m)
{
	it=begin(u_m);
	advance(it,step);
}
/*
void update_matrix_variance(){
	int total_items = map_rating.size();
	//int numthreads = 4;
	unordered_map<string,unordered_map<string,decimal>>::iterator fit_i;
	//# pragma omp parallel for num_threads(numthreads) private(fit_i) //shared(matrix_desviations,total_items) 
	for(int i=0; i<total_items; i++)
	{
		unordered_map<string,unordered_map<string,decimal>>::iterator fit_j;
		set_iter(fit_i,i,map_rating);
		cout<<i<<" first for "<< omp_get_thread_num()<<endl;
		set_iter(fit_j,i,map_rating);
		# pragma omp parallel for private(fit_j) shared(matrix_desviations)
		for (int j = i; j < total_items; j++)
		{	
			set_iter(fit_j,j,map_rating);
			cout<<"second for "<< omp_get_thread_num()<<endl;
			decimal this_variance = get_variance(fit_i->first,fit_j->first);
			matrix_desviations[fit_i->first][fit_j->first]=this_variance;
			matrix_desviations[fit_j->first][fit_i->first]=-this_variance;
		}	
	}
	
}*/
void update_matrix_variance_iterative(){
	int total_items = map_rating.size();
	auto fit_i =begin(map_rating);
	for(int i=0; i<total_items; i++)
	{
		auto fit_j=begin(map_rating);
		advance(fit_j,i);
		for (int j = i; j < total_items; j++)
		{
			auto this_variance = get_variance(fit_i->first,fit_j->first);
			matrix_desviations[fit_i->first][fit_j->first]=this_variance;
			this_variance.second=-this_variance.second;
			matrix_desviations[fit_j->first][fit_i->first]=this_variance;
			fit_j++;
		}
		fit_i++;	
	}	
}
void matrix_variance_for_one(string item){
	int total_items = map_rating.size();
	auto fit_i =map_rating.find(item);
	auto fit_j=begin(map_rating);
	
	for (int j = 0; j < total_items; j++)
	{
		auto this_variance = get_variance(fit_i->first,fit_j->first);
		matrix_desviations[fit_i->first][fit_j->first]=this_variance;
		this_variance.second=-this_variance.second;
		matrix_desviations[fit_j->first][fit_i->first]=this_variance;
		fit_j++;
	}

	
}
void prediction(string user,string item)
{	
	decimal numerator = 0;
	decimal denominator = 0;
	for(auto item_i:map_rating){
		auto found = item_i.second.find(user); 
		if(found!=end(item_i.second)){
			auto temp = matrix_desviations[item][item_i.first];
			numerator+=(found->second+temp.second)*temp.first;
			denominator+=temp.first;
		}
	}
	cout<<numerator/denominator<<endl;
}
int main()
{
	auto start = std::chrono::system_clock::now();

	load_data();
	/*map_rating ={{"Taylor",{{"Amy",4},{"Ben",5},{"Daisy",5}}},
		{"PSY",{{"Amy",3},{"Ben",2},{"Clara",3.5}}},
		{"Whitney",{{"Amy",4},{"Clara",4},{"Daisy",3}}}
	};*/
	auto end = std::chrono::system_clock::now();
	std::chrono::duration<double> elapsed_seconds = end-start;
    std::cout << "la carga de datos a tardado: " << elapsed_seconds.count() << "s\n";
	string user = "1";
	string item = "29";
	

	start = std::chrono::system_clock::now();
	//update_matrix_variance_iterative();
	matrix_variance_for_one(item);

	cout<<"size "<<map_rating.size()<<endl;

	cout<<"matrix size "<<matrix_desviations.size()<<endl;
	/*
	for(auto i:matrix_desviations){
		for(auto j:i.second){
			cout<<"| |"<<i.first<<"| |"<<j.first<<" "<<j.second.second<<endl;
		}
	}*/

	prediction(user,item);
	end = std::chrono::system_clock::now();
	elapsed_seconds = end-start;
    std::cout << "la prediccion a tardado: " << elapsed_seconds.count() << "s\n";
	
/*
	
	int opt = -2;  // -1 -> pearson   |  -2-> coseno
	int k = 4;
	int k2;
	cout<<"START: "<<endl;
	while(getline(cin,name)){
	
		if (name.empty()) continue;
	    istringstream is(name);
	
		map_knn.clear();
		map_recomendacion.clear();
		map_proyeccion.clear();
		cout<<name<<endl;
		cout<<"option: ";
		cin>>opt;	cout<<opt<<endl;
		cout<<" K : ";
		cin>>k;
		cout<<k<<endl;
		cout<<"Recomendacion: ";
		cin>>k2;	cout<<k2<<endl;

		start = std::chrono::system_clock::now();

		k_nn(name,opt);
		//cout<<map_knn.size()<<endl;
		print_knn(k,opt);
		//proyeccion(bookn,k,opt);
		recomendacion(name,k2);
		end = std::chrono::system_clock::now();
		std::chrono::duration<double> elapsed_seconds = end-start;
		std::cout<< "la consulta a tardado: " << elapsed_seconds.count() << "s\n";
				
		cout<<"TAM: "<<map_recomendacion.size()<<endl;

		cout<<"***************************"<<endl;
	}
*/
        return 1;
}

# get networks stats
# run this after osmnx_generate_networks_vx.py
import pickle
target_folder = "C:\\networks"
networks = pickle.load( open( target_folder + "\\networks_stats.pkl", "rb" ) )
for town,stats in networks.items():
    print (town,'nodes',stats['n'],'edges',stats['m'],'area km2',round(stats['areakm2'],2),'edge dens',round(stats['edge_density_km'],2),'node den',round(stats['node_density_km'],2))
    

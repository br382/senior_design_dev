For sending msg to server using these:
	{'update_user':marker_struct}
	{'update_marker':marker_struct}
	{'update_pos':marker_struct}

each struct requires a {'last_modify':'string'} style timestamp for server acceptance and a {'uid':000} style uid for knowing where to place it.
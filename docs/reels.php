<?php
function get_posts($args = [])
{
    global $db, $system, $redis;
    $me = $this->_data['user_id'];
    $posts = null;
    $ids__ = false;

    if (isset($args['posts'])) {
        $postss_ = explode(',', $args['posts']);
        foreach ($postss_ as $integer) {
            if (intval($integer)) {
                $ids[] = $integer;
            }
        }
        $ids = @implode(',', $ids);
        $ids__ = true;
    }

    $args['offset'] = ($args['offset'] >= 0) ? $args['offset'] : 0;

    $posts_cookie = (!empty($_COOKIE['posts']) ? $_COOKIE['posts'] : 'seguindo');

    if ($_COOKIE['posts_minutos'] != 'posts_minutos' and !empty($_SESSION['posts_minutos']) and $get == 'newsfeed' and $get == 'posts_group' and $this->_logged_in) {
        unset($_SESSION['posts_minutos']);
        unset($_COOKIE['posts_minutos']);
    }

    /* validate arguments */
    $get = !isset($args['get']) ? 'newsfeed' : $args['get'];
    $filter = !isset($args['filter']) ? 'all' : $args['filter'];
    if (!in_array($filter, array('all', '', 'link', 'live', 'media', 'photos', 'video', 'audio', 'file', 'poll', 'product', 'article', 'map'))) {
        _error(400);
    }

    $last_post_id = !isset($args['last_post_id']) ? null : $args['last_post_id'];
    if (isset($args['last_post']) && !is_numeric($args['last_post'])) {
        _error(400);
    }

    $offset = !isset($args['offset']) ? '0' : $args['offset'];

    $system['max_results'] = 6;

    $offset *= $system['max_results'];

    $get_all = !isset($args['get_all']) ? false : true;

    if (isset($args['query'])) {
        if (is_empty($args['query'])) {
            return $posts;
        } else {
            $query = secure($args['query'], 'search_tag', true);
        }
    }


    if ($args['get'] == 'newsfeed') {
        $order_query = " ORDER BY posts.interacao DESC";
    } else {
        $order_query = " ORDER BY posts.post_id DESC";
    }

    /* get posts */
    switch ($get) {
        case 'newsfeed':
            if (!$this->_logged_in) {

                //usuários não poderão ver posts de contas desativadas
                $where_query .= " INNER JOIN users ON ( posts.user_id = users.user_id AND posts.user_type ='user' AND users.user_verified = '1' ) WHERE (";

                $where_query .= " posts.privacy = 'public'";
                $where_query .= ")";
            } else {

                $where_query .= " WHERE (";

                /* get viewer posts */
                if (empty($query)) {

                    $where_query .= " ( posts.user_id = $me AND posts.user_type = 'user' )";
                } else {

                    // Search for hashtags
                    $hashtags = secure($args['query'], 'search_tag', true);
                    $where_query .= " MATCH(posts.hashtags) AGAINST ($hashtags IN BOOLEAN MODE) AND posts.privacy = 'public' AND posts.hashtags_atualizado = '1' ";
                }

                if (empty($query)) {

                    if ($this->_data['user_group'] == 3) {

                        // grupos
                        if ($this->_data['groups_ids']) {
                            $groups_list = array_unique($this->_data['groups_ids']);
                            $groups_list = implode(',', $groups_list);
                            $where_query .= " OR ( posts.group_id IN($groups_list) AND posts.in_group = '1' )";
                        }
                        // grupos



                        // pages
                        $paginas = $this->_data['pages_ids'];

                        // Se tiver parceiros e páginas junta tudo
                        if ($this->_data['get_pages_ids_parceiros'] && $paginas) {

                            $paginas = array_merge($this->_data['get_pages_ids_parceiros'], $paginas);
                        }

                        // Se tiver parceiros e não tiver páginas só atribui os parceiros
                        if ($this->_data['get_pages_ids_parceiros'] && !$paginas) {

                            $paginas = $this->_data['get_pages_ids_parceiros'];
                        }

                        // Se tiver páginas para ocultar e páginas atribui só a diferença
                        if ($this->_data['get_page_unfollowed'] && $paginas) {

                            $paginas = array_diff($paginas, $this->_data['get_page_unfollowed']);
                        }

                        if ($paginas) {

                            $pages_list = array_unique($paginas);

                            $pages_list = implode(',', $pages_list);
                            $where_query .= " OR ( posts.user_id IN($pages_list) AND posts.user_type = 'page' )";
                        }
                        // pages



                        if ($get == 'newsfeed') {
                            $hashtags = $this->_data['following_hashtag'];
                            if (!empty($hashtags)) {
                                foreach ($hashtags as $hashtag) {
                                    $hash = secure($hashtag, 'search');
                                    $where_query .= " OR ( posts.hashtags LIKE $hash AND posts.privacy = 'public' AND posts.hashtags_atualizado = '1' ) ";
                                }
                            }
                        }


                        // remove os ocultados dos seguidores
                        if (!empty($this->_data['followings_ids']) && !empty($this->_data['ocultados'])) {
                            $ocultadosList = array_diff($this->_data['followings_ids'], $this->_data['ocultados']);

                            if (!empty($ocultadosList)) {
                                $ocultadosList = array_unique($ocultadosList);

                                if ($this->_data['seguir_users_ocultos']) {
                                    $ocultadosList = array_diif($this->_data['seguir_users_ocultos'], $ocultadosList);
                                }

                                $follw_array = implode(',', $ocultadosList);
                                $where_query .= " OR ( posts.user_id IN ( $follw_array ) AND posts.user_type = 'user' AND posts.privacy = 'public' )";
                            }

                            //exibe apenas os usuários que está seguindo
                        } elseif (!empty($this->_data['followings_ids'])) {
                            $this->_data['followings_ids'] = array_unique($this->_data['followings_ids']);

                            if (!empty($this->_data['followings_ids'])) {

                                if ($this->_data['seguir_users_ocultos']) {

                                    $follw_array = array_merge($this->_data['followings_ids'], $this->_data['seguir_users_ocultos']);
                                } else {

                                    $follw_array = $this->_data['followings_ids'];
                                }

                                $follw_array = implode(',', $follw_array);
                                $where_query .= " OR ( posts.user_id IN ( $follw_array ) AND posts.user_type = 'user' AND posts.privacy = 'public' )";
                            }
                        } elseif (!empty($this->_data['seguir_users_ocultos'])) {

                            $follw_array = implode(',', $this->_data['seguir_users_ocultos']);

                            $where_query .= " OR ( posts.user_id IN ( $follw_array ) AND posts.user_type = 'user' AND posts.privacy = 'public' )";
                        }
                    } else {

                        $where_query .= " OR ( posts.privacy = 'public' )";
                    }
                }

                $where_query .= ")";
            }

            break;
        case 'posts_profile':
            if (isset($args['id']) && !is_numeric($args['id'])) {
                _error(400);
            }
            $id = $args['id'];

            if ($this->_logged_in) {

                if ($id == $this->_data['user_id']) {

                    $where_query .= " WHERE ( posts.user_id = $id AND posts.user_type = 'user' ) ";
                } else {

                    if ($this->_data['user_group'] == '3') {

                        $where_query .= " WHERE ( posts.user_id = $id AND posts.user_type = 'user' AND posts.privacy = 'public' ) ";
                    } else {

                        $where_query .= " WHERE ( posts.user_id = $id AND posts.user_type = 'user' ) ";
                    }
                }
            } else {

                $where_query .= " WHERE ( posts.user_id = $id AND posts.user_type = 'user' AND posts.privacy = 'public' ) ";
            }

            break;
        case 'posts_page':
            if (isset($args['id']) && !is_numeric($args['id'])) {
                _error(400);
            }
            $id = $args['id'];
            $where_query .= "WHERE ( posts.user_id = $id AND posts.user_type = 'page' )";
            break;
        case 'posts_group':
            if (isset($args['id']) && !is_numeric($args['id'])) {
                _error(400);
            }
            $id = $args['id'];
            $ids_grupo = $this->get_grupos_removido($id);

            if (!empty($this->_data['ocultados']) && !empty($ids_grupo)) {

                $ocultadosList = array_merge($this->_data['ocultados'], $ids_grupo);
                $ocultadosList = array_unique($ocultadosList);
                $ids_grupo = @implode(',', $ocultadosList);
                $where_query .= " WHERE ( group_id = $id AND in_group = '1' AND posts.user_id NOT IN ($ids_grupo) )";
            } elseif (!empty($this->_data['ocultados'])) {

                $ocultadosList = $this->_data['ocultados'];
                $ocultadosList = array_unique($ocultadosList);
                $ids_grupo = @implode(',', $ocultadosList);
                $where_query .= " WHERE ( group_id = $id AND in_group = '1' AND posts.user_id NOT IN ($ids_grupo) )";
            } else {

                $where_query .= " WHERE ( group_id = $id AND in_group = '1' )";
            }

            break;
        case 'boosted':
            $id = $this->_data['user_id'];

            if ($args['boosted_aprovado']) {

                $system['max_results'] = 5;

                $where_query .= " WHERE ( boosted = '1' AND post_boosted_approved = '0' )";
            } else {
                $where_query .= " WHERE ( boosted = '1' AND boosted_by = $id )";
            }

            break;
        case 'saved':
            $id = $this->_data['user_id'];
            $where_query .= "INNER JOIN posts_saved ON posts.post_id = posts_saved.post_id WHERE (posts_saved.user_id = $id)";
            break;

        default:
            _error(400);
            break;
    }


    if ($get == 'newsfeed' or $get == 'posts_group') {

        if (empty($query)) {

            if ($redis->get("posts_cache-{$this->_data['user_id']}")) {
                $cookies_ = unserialize($redis->get("posts_cache-{$this->_data['user_id']}"));
            }

            //tem redis no _get_hidden_posts()
            $hidden = $this->_get_hidden_posts($this->_data['user_id']);
            $hiddenPosts = [];


            if (!empty($cookies_) and !empty($hidden)) {

                $hiddenPosts = @array_merge($hidden, $cookies_);
            } elseif (!empty($cookies_) and empty($hidden)) {

                $hiddenPosts = $cookies_;
            } elseif (!empty($hidden) and empty($cookies_)) {

                $hiddenPosts = $hidden;
            }

            if (!empty($hiddenPosts)) {
                $hiddenPostsList = array_unique($hiddenPosts);
                $posts_to_hidden = @implode(',', $hiddenPostsList);
            }

            if ($posts_to_hidden) {

                $where_query .= " AND ( posts.post_id NOT IN( $posts_to_hidden ) )";
                // AND posts.origin_id NOT IN( $posts_to_hidden )
            }
        }

        if ($filter != "all") {
            $where_query .= " AND ( posts.post_type = '$filter')";
        }

        if (!empty($this->_data['get_page_unfollowed'])) {
            $page_unfollowed = array_unique($this->_data['get_page_unfollowed']);
            $get_page_unfollowed = implode(',', $page_unfollowed);
            $where_query .= " AND ( posts.user_id NOT IN( $get_page_unfollowed AND posts.user_type = 'page' ) )";
        }
    }

    // nunca remover esta LINHA, vai travar tudo !
    $where_query .= "
AND posts.post_bloqueado = '0'
AND posts.post_type NOT IN('profile_picture','profile_cover','page_cover','page_picture')
";
    // nunca remover esta LINHA!

    $limit_statement = ($get_all) ? "" : sprintf("LIMIT %s, %s", secure($offset, 'int', false), secure($system['max_results'], 'int', false));

    $get_posts = $db->query("SELECT posts.post_id FROM posts " . $where_query . " " . $order_query . " " . $limit_statement) or _error(SQL_ERROR_THROWEN);

    $con = 0;

    if ($get_posts->num_rows > 0) {
        while ($postsss = $get_posts->fetch_assoc()) {

            $ids_[] = $postsss['post_id'];

            $con++;
            if (!$this->_logged_in) {
                $post = $this->get_post($postsss['post_id'], true, true);

                if ($post) {
                    $posts[$con] = $post;
                }
            } elseif ($con == '1' and $get == 'newsfeed' and $posts_cookie == 'global' and empty($query)) {
                if ($get == 'newsfeed' and $posts_cookie == 'global') {
                    if (!empty($posts_star['post_id'])) {
                        $post = $this->get_post($posts_star['post_id'], true, true);
                        if ($post) {
                            $posts[$con] = $post;
                        }
                    }
                }

                // or $con == '7' or $con == '13' or $con == '19'
            } elseif ($con == '2' or $con == '7' and $get == 'newsfeed' and $get == 'posts_group' and empty($query)) {

                if ($args['get'] != 'posts_profile' and $args['get'] != 'posts_page' and $args['get'] != 'posts_group' and $get != 'boosted' and !$query) {

                    $po_st = $this->get_boosted_post();

                    if ($po_st['post_id']) {
                        $po_st['patrocinado'] = true;
                        $posts[$con] = $po_st;

                        //coloca post patrocinado dentro do redis
                        $ids_[] = $po_st['post_id'];
                        //coloca post patrocinado dentro do redis

                        $con++;

                        $post = $this->get_post($postsss['post_id'], true, true);
                        if ($post['post_id']) {
                            $posts[$con] = $post;

                            if ($post['origin_id']) {
                                $ids_[] = $post['origin_id'];
                            }
                        }
                    }
                } else {
                    $post = $this->get_post($postsss['post_id'], true, true);
                    if ($args['get'] == 'posts_group') {
                        $post['group_id'] = $args['id'];
                    }
                    if ($post['post_id']) {
                        $posts[$con] = $post;

                        if ($post['origin_id']) {
                            $ids_[] = $post['origin_id'];
                        }
                    }
                }
            } else {
                $post = $this->get_post($postsss['post_id'], true, true);
                if ($post) {
                    $posts[$con] = $post;

                    if ($post['origin_id']) {
                        $ids_[] = $post['origin_id'];
                    }
                }
            }
        }
    } else {
        if ($redis->get("posts_cache-{$this->_data['user_id']}")) {
            $redis->delete("posts_cache-{$this->_data['user_id']}");
        }
        return;
    }
    if ($get == 'newsfeed' or $get == 'posts_group') {

        if (!$redis->get("posts_cache-{$this->_data['user_id']}")) {
            $ids_ = array_unique($ids_);
            $redis->set("posts_cache-{$this->data['user_id']}", serialize($ids));
            $redis->expire("posts_cache-{$this->_data['user_id']}", 60 * 60 * 1);
        } else {
            $posts_cached = unserialize($redis->get("posts_cache-{$this->_data['user_id']}"));
            $posts_cached = array_merge($ids_, $posts_cached);
            $posts_cached = array_unique($posts_cached);
            $redis->set("posts_cache-{$this->_data['user_id']}", serialize($posts_cached));
            $redis->expire("posts_cache-{$this->_data['user_id']}", 60 * 60 * 1);
        }
    }
    return $posts;
}

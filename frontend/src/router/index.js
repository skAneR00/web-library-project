import { createRouter, createWebHistory } from 'vue-router'
import { adminAuth } from '../services/adminAuth'
import AdminView from '../views/AdminView.vue'
import BookCreateView from '../views/BookCreateView.vue'
import BookEditView from '../views/BookEditView.vue'
import BooksLayout from '../views/BooksLayout.vue'
import BooksView from '../views/BooksView.vue'
import CollectionsView from '../views/CollectionsView.vue'
import FavoritesView from '../views/FavoritesView.vue'
import HomeView from '../views/HomeView.vue'
import NotFoundView from '../views/NotFoundView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/books',
      component: BooksLayout,
      children: [
        {
          path: '',
          name: 'books',
          component: BooksView,
        },
        {
          path: 'collections',
          name: 'book-collections',
          component: CollectionsView,
        },
      ],
    },
    {
      path: '/favorites',
      name: 'favorites',
      component: FavoritesView,
    },
    {
      path: '/admin',
      name: 'admin',
      component: AdminView,
    },
    {
      path: '/admin/books/new',
      name: 'admin-book-new',
      component: BookCreateView,
      meta: { requiresAdmin: true },
    },
    {
      path: '/admin/books/:id/edit',
      name: 'admin-book-edit',
      component: BookEditView,
      props: true,
      meta: { requiresAdmin: true },
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: NotFoundView,
    },
  ],
})

router.beforeEach((to) => {
  if (to.meta.requiresAdmin && !adminAuth.isAuthenticated()) {
    return { name: 'admin' }
  }
})

export default router

import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import UserProfile from '../../components/UserProfile';
import DiscussionList from '../../components/DiscussionList';
import { fetchUser, fetchUserDiscussions } from '../../utils/api';

export default function UserPage({ token }) {
  const router = useRouter();
  const { id } = router.query;
  const [user, setUser] = useState(null);
  const [discussions, setDiscussions] = useState([]);

  useEffect(() => {
    if (id) {
      const loadUser = async () => {
        const data = await fetchUser(id);
        setUser(data);
      };
      const loadDiscussions = async () => {
        const data = await fetchUserDiscussions(id);
        setDiscussions(data);
      };
      loadUser();
      loadDiscussions();
    }
  }, [id]);

  if (!user) return <div>Loading...</div>;

  return (
    <div className="container">
      <UserProfile user={user} />
      <h2>User Discussions</h2>
      <DiscussionList discussions={discussions} token={token} />
    </div>
  );
}

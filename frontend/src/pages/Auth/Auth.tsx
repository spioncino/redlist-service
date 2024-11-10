import { motion } from 'framer-motion';
import css from './Auth.module.css';
import { AuthTip } from '../../components';

const Auth = () => {
  return (
    <form className={css.mainContainer}>
      <AuthTip />
      <motion.div layout className={css.authContainer}>
        <h3>Вход</h3>
        <hr />
        <p>
          Код<span>*</span>
        </p>
        <form className={css.authContentForm}>
          <input
            className={css.authContentInput}
            maxLength={40}
            placeholder="Уникальный 48-ми значный код"
          />
        </form>
        <span className={css.buttonContent}>
          <button type="submit">Войти</button>
        </span>
      </motion.div>
    </form>
  );
};

export default Auth;
